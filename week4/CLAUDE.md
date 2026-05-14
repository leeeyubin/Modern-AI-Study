# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All commands must be run from the `week4/` directory with the Conda environment (`cs146s`) activated and dependencies installed via `poetry install` from the repo root.

```bash
make run      # Start FastAPI dev server at http://127.0.0.1:8000 (auto-reload)
make test     # Run all tests with pytest
make lint     # Run ruff linter
make format   # Auto-format with black + ruff --fix
make seed     # Seed the SQLite database (only runs if data/app.db doesn't exist)
```

Run a single test file:
```bash
PYTHONPATH=. pytest -q backend/tests/test_notes.py
```

Set up pre-commit hooks (required once per clone):
```bash
pre-commit install
pre-commit run --all-files  # validate entire repo
```

## Architecture

**Stack:** FastAPI + SQLAlchemy 2.x + SQLite + vanilla JS frontend. No ORM relationships — all queries use `select()` directly.

**Request flow:**
```
frontend/index.html + app.js
    → FastAPI routes (backend/app/routers/)
    → SQLAlchemy Session via get_db() dependency (backend/app/db.py)
    → SQLite at data/app.db
```

**Key design decisions:**
- `get_db()` is a FastAPI dependency (yields a session with auto-commit/rollback). `get_session()` is a context manager for use outside of request handlers (e.g., seeding).
- `DATABASE_PATH` env var (or `.env` file) overrides the default `./data/app.db` path. Tests override `get_db` via `app.dependency_overrides` and use a temp SQLite file per test.
- The database is seeded automatically on first run (`apply_seed_if_needed` in `startup_event`) from `data/seed.sql`.
- Pydantic schemas (`schemas.py`) are separate from SQLAlchemy models (`models.py`). Use `.model_validate(orm_obj)` to convert.
- `backend/app/services/extract.py` contains text-parsing logic (currently extracts action items from note content based on `!` suffix or `todo:` prefix).

**Models:**
- `Note`: `id`, `title` (str ≤200), `content` (text)
- `ActionItem`: `id`, `description` (text), `completed` (bool, default False)

**API routes:**
- `GET/POST /notes/` — list and create notes
- `GET /notes/search/?q=` — search notes by title or content
- `GET /notes/{id}` — get a single note
- `GET/POST /action-items/` — list and create action items
- `PUT /action-items/{id}/complete` — mark an action item complete

**Frontend** is served as static files mounted at `/static`; `GET /` returns `frontend/index.html`.

## Linting & Formatting

- Line length: 100 (black + ruff)
- Ruff rules enabled: `E`, `F`, `I`, `UP`, `B` (with `E501` and `B008` ignored)
- Pre-commit hooks enforce black, ruff --fix, end-of-file newlines, and trailing whitespace

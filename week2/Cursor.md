# Week 2 - Action Item Extractor

## Overview

This project is a FastAPI application that converts free-form notes into actionable tasks.

It supports two extraction modes:
- **Rule-based extraction** using lightweight text heuristics.
- **LLM-based extraction** using Ollama (`llama3.1:8b`) for structured action item generation.

Extracted items and notes are stored in SQLite, and a small web UI is provided for manual interaction.

## Project Structure

- `app/main.py`: FastAPI app setup, lifecycle hooks, router registration, frontend/static serving
- `app/routers/`: API route handlers for notes and action items
- `app/services/extract.py`: rule-based and LLM extraction logic
- `app/db.py`: SQLite initialization and data access helpers
- `app/schemas.py`: request/response models
- `frontend/`: browser UI (`index.html`)
- `tests/`: unit tests for extraction logic

## Setup and Run

### 1) Install dependencies

From the repository root:

```bash
poetry install
```

### 2) (Optional) Activate course environment

If you are following the course environment setup:

```bash
conda activate cs146s
```

### 3) Run the server

From the repository root:

```bash
poetry run uvicorn week2.app.main:app --reload
```

Open:

- App UI: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4) Ollama requirement for LLM extraction

The `POST /action-items/extract-llm` endpoint uses Ollama. Make sure Ollama is installed, running, and the model is available:

```bash
ollama run llama3.1:8b
```

## API Endpoints

### Root and Static

- `GET /`
  - Returns the frontend HTML page.
- `GET /static/*`
  - Serves static frontend assets.

### Notes

- `POST /notes`
  - Create a note.
  - Request body:
    ```json
    { "content": "Sprint planning notes..." }
    ```
  - Returns created note (`id`, `content`, `created_at`).
  - Returns `400` if `content` is blank.

- `GET /notes`
  - List all notes.
  - Returns an array of notes.

- `GET /notes/{note_id}`
  - Get a single note by ID.
  - Returns `404` if the note does not exist.

### Action Items

- `POST /action-items/extract`
  - Extract action items using rule-based logic.
  - Request body:
    ```json
    { "text": "- [ ] Set up CI\n- Write tests", "save_note": true }
    ```
  - Behavior:
    - Validates non-empty text.
    - Optionally saves source text as a note.
    - Extracts action items and stores them in DB.
  - Response:
    ```json
    {
      "note_id": 1,
      "items": [
        { "id": 10, "text": "Set up CI" },
        { "id": 11, "text": "Write tests" }
      ]
    }
    ```

- `POST /action-items/extract-llm`
  - Extract action items using Ollama LLM.
  - Request/response shape is the same as `/action-items/extract`.
  - Returns `400` if `text` is blank.

- `GET /action-items`
  - List action items.
  - Optional query parameter: `note_id`
    - Example: `GET /action-items?note_id=1`
  - Returns:
    - `id`
    - `note_id`
    - `text`
    - `done`
    - `created_at`

- `POST /action-items/{action_item_id}/done`
  - Mark an action item done/undone.
  - Request body:
    ```json
    { "done": true }
    ```
  - Response:
    ```json
    { "id": 10, "done": true }
    ```

## Running Tests

This project uses `pytest`.

From the repository root, run:

```bash
poetry run pytest week2/tests
```

Or run the extraction test file directly:

```bash
poetry run pytest week2/tests/test_extract.py
```

## Notes

- LLM endpoint behavior depends on local Ollama availability and model readiness.
- Unit tests for LLM extraction mock Ollama calls, so tests do not require a live model.

# API Reference

**Title:** Modern Software Dev Starter (Week 4)  
**Version:** 0.1.0  
**OpenAPI:** 3.1.0

---

## Notes

### `GET /notes/`

List all notes.

**Response 200**
- `id` — integer
- `title` — string
- `content` — string

---

### `POST /notes/`

Create a new note.

**Request body** (required)
- `title` — string (required)
- `content` — string (required)

**Response 201**
- `id` — integer
- `title` — string
- `content` — string

**Response 422** — Validation Error

---

### `GET /notes/search/`

Search notes by title or content.

**Query parameters**
- `q` — string | null (optional)

**Response 200** — array of notes
- `id` — integer
- `title` — string
- `content` — string

**Response 422** — Validation Error

---

### `GET /notes/{note_id}`

Get a single note by ID.

**Path parameters**
- `note_id` — integer (required)

**Response 200**
- `id` — integer
- `title` — string
- `content` — string

**Response 422** — Validation Error

---

## Action Items

### `GET /action-items/`

List all action items.

**Response 200** — array of action items
- `id` — integer
- `description` — string
- `completed` — boolean

---

### `POST /action-items/`

Create a new action item.

**Request body** (required)
- `description` — string (required)

**Response 201**
- `id` — integer
- `description` — string
- `completed` — boolean

**Response 422** — Validation Error

---

### `PUT /action-items/{item_id}/complete`

Mark an action item as complete.

**Path parameters**
- `item_id` — integer (required)

**Response 200**
- `id` — integer
- `description` — string
- `completed` — boolean

**Response 422** — Validation Error

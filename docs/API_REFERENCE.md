# PromptLab API Reference

Comprehensive documentation for every backend endpoint that PromptLab currently exposes. The API is unauthenticated and designed for fast iteration.

---

## General Notes

- **Base URL**: `http://localhost:8000`
- **Docs**: Swagger/OpenAPI at `/docs`
- **Authentication**: None required for local development.
- All request and response bodies use JSON.

---

## Health Check

### GET `/health`

`GET /health` verifies that the API is running and reports the current package version.

#### Request
```bash docs/API_REFERENCE.md
curl http://localhost:8000/health
```

#### Response (200)
```json docs/API_REFERENCE.md
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

## Prompt Endpoints

### GET `/prompts`

List prompts with optional filtering and search. Results are sorted with the newest items first.

#### Query Parameters

| Name | Type | Description |
|------|------|-------------|
| `collection_id` | string | Filter prompts for a specific collection UUID. |
| `search` | string | Case-insensitive search in the prompt title and description. |

#### Request
```bash docs/API_REFERENCE.md
curl "http://localhost:8000/prompts?search=summary&collection_id=release-notes"
```

#### Response (200)
```json docs/API_REFERENCE.md
{
  "prompts": [
    {
      "id": "d417c8c0-6d1c-4aaf-bc03-7c6de0f1e3f7",
      "title": "Summarize release notes",
      "content": "Summarize the release: {{input}}",
      "description": "Used for weekly distribution",
      "collection_id": "cb80f39e-9594-4f71-8301-d18d9c7b1c3a",
      "created_at": "2025-01-10T12:34:56.789000",
      "updated_at": "2025-01-10T12:34:56.789000"
    }
  ],
  "total": 1
}
```

### GET `/prompts/{id}`

Retrieve a single prompt.

#### Request
```bash docs/API_REFERENCE.md
curl http://localhost:8000/prompts/d417c8c0-6d1c-4aaf-bc03-7c6de0f1e3f7
```

#### Response (200)
```json docs/API_REFERENCE.md
{
  "id": "d417c8c0-6d1c-4aaf-bc03-7c6de0f1e3f7",
  "title": "Summarize release notes",
  "content": "Summarize the release: {{input}}",
  "description": "Used for weekly distribution",
  "collection_id": "cb80f39e-9594-4f71-8301-d18d9c7b1c3a",
  "created_at": "2025-01-10T12:34:56.789000",
  "updated_at": "2025-01-10T12:34:56.789000"
}
```

### POST `/prompts`

Create a new prompt template.

#### Request
```bash docs/API_REFERENCE.md
curl -X POST http://localhost:8000/prompts \
  -H 'Content-Type: application/json' \
  -d '{"title": "Executive summary prep", "content": "Produce a slide summary for {{input}}", "description": "Template for exec teams", "collection_id": "cb80f39e-9594-4f71-8301-d18d9c7b1c3a"}'
```

#### Response (201)
```json docs/API_REFERENCE.md
{
  "id": "5b5dd8a5-1e8f-4ee2-a1e4-0c8f8c0be1b8",
  "title": "Executive summary prep",
  "content": "Produce a slide summary for {{input}}",
  "description": "Template for exec teams",
  "collection_id": "cb80f39e-9594-4f71-8301-d18d9c7b1c3a",
  "created_at": "2025-02-01T09:00:00.000000",
  "updated_at": "2025-02-01T09:00:00.000000"
}
```

### PUT `/prompts/{id}`

Replace an existing prompt. The payload must include all prompt attributes.

#### Request
```bash docs/API_REFERENCE.md
curl -X PUT http://localhost:8000/prompts/5b5dd8a5-1e8f-4ee2-a1e4-0c8f8c0be1b8 \
  -H 'Content-Type: application/json' \
  -d '{"title": "Executive summary prep", "content": "Summarize {{input}} for leadership", "description": "Updated tone", "collection_id": "cb80f39e-9594-4f71-8301-d18d9c7b1c3a"}'
```

#### Response (200)
```json docs/API_REFERENCE.md
{
  "id": "5b5dd8a5-1e8f-4ee2-a1e4-0c8f8c0be1b8",
  "title": "Executive summary prep",
  "content": "Summarize {{input}} for leadership",
  "description": "Updated tone",
  "collection_id": "cb80f39e-9594-4f71-8301-d18d9c7b1c3a",
  "created_at": "2025-02-01T09:00:00.000000",
  "updated_at": "2025-02-01T10:30:00.000000"
}
```

### PATCH `/prompts/{id}`

Modify only the fields that are provided.

#### Request
```bash docs/API_REFERENCE.md
curl -X PATCH http://localhost:8000/prompts/5b5dd8a5-1e8f-4ee2-a1e4-0c8f8c0be1b8 \
  -H 'Content-Type: application/json' \
  -d '{"description": "Executive tone for board review"}'
```

#### Response (200)
```json docs/API_REFERENCE.md
{
  "id": "5b5dd8a5-1e8f-4ee2-a1e4-0c8f8c0be1b8",
  "title": "Executive summary prep",
  "content": "Summarize {{input}} for leadership",
  "description": "Executive tone for board review",
  "collection_id": "cb80f39e-9594-4f71-8301-d18d9c7b1c3a",
  "created_at": "2025-02-01T09:00:00.000000",
  "updated_at": "2025-02-01T11:05:00.000000"
}
```

### DELETE `/prompts/{id}`

Delete a prompt permanently.

#### Request
```bash docs/API_REFERENCE.md
curl -X DELETE http://localhost:8000/prompts/5b5dd8a5-1e8f-4ee2-a1e4-0c8f8c0be1b8
```

#### Response (204)
No body is returned when the delete succeeds.

---

## Collection Endpoints

### GET `/collections`

List all collections.

#### Request
```bash docs/API_REFERENCE.md
curl http://localhost:8000/collections
```

#### Response (200)
```json docs/API_REFERENCE.md
{
  "collections": [
    {
      "id": "cb80f39e-9594-4f71-8301-d18d9c7b1c3a",
      "name": "Release Notes",
      "description": "Prompts related to release summaries",
      "created_at": "2024-12-01T08:00:00.000000"
    }
  ],
  "total": 1
}
```

### GET `/collections/{id}`

Retrieve a single collection.

#### Request
```bash docs/API_REFERENCE.md
curl http://localhost:8000/collections/cb80f39e-9594-4f71-8301-d18d9c7b1c3a
```

#### Response (200)
```json docs/API_REFERENCE.md
{
  "id": "cb80f39e-9594-4f71-8301-d18d9c7b1c3a",
  "name": "Release Notes",
  "description": "Prompts related to release summaries",
  "created_at": "2024-12-01T08:00:00.000000"
}
```

### POST `/collections`

Create a collection for grouping prompts.

#### Request
```bash docs/API_REFERENCE.md
curl -X POST http://localhost:8000/collections \
  -H 'Content-Type: application/json' \
  -d '{"name": "Release Notes", "description": "Prompts for summarizing product launches."}'
```

#### Response (201)
```json docs/API_REFERENCE.md
{
  "id": "cb80f39e-9594-4f71-8301-d18d9c7b1c3a",
  "name": "Release Notes",
  "description": "Prompts for summarizing product launches.",
  "created_at": "2024-12-01T08:00:00.000000"
}
```

### DELETE `/collections/{id}`

Delete a collection. All prompts assigned to the collection are disassociated (collection_id set to `null`).

#### Request
```bash docs/API_REFERENCE.md
curl -X DELETE http://localhost:8000/collections/cb80f39e-9594-4f71-8301-d18d9c7b1c3a
```

#### Response (204)
No body is returned when the delete succeeds.

---

## Error Handling

| Status | Description | Payload |
|--------|-------------|---------|
| 400 | Bad request (e.g., referencing missing collection) | `{"detail": "Collection not found"}` |
| 404 | Resource not found | `{"detail": "Prompt not found"}` or similar |

### Example: Invalid Collection on Prompt Creation
```bash docs/API_REFERENCE.md
curl -X POST http://localhost:8000/prompts \
  -H 'Content-Type: application/json' \
  -d '{"title": "Bad collection", "content": "{{input}}", "collection_id": "invalid"}'
```

#### Response (400)
```json docs/API_REFERENCE.md
{
  "detail": "Collection not found"
}
```

### Example: Missing Prompt
```bash docs/API_REFERENCE.md
curl http://localhost:8000/prompts/00000000-0000-0000-0000-000000000000
```

#### Response (404)
```json docs/API_REFERENCE.md
{
  "detail": "Prompt not found"
}
```

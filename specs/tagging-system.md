# Tagging System Feature Specification

## Overview & Goals

PromptLab needs a flexible tagging system so engineers can categorize prompts by discipline, intent, or experimentation batch. Tags should be lightweight, searchable, and combinable with collections for filtering.

Goals:

- Allow prompts to carry zero or more tags (strings).
- Provide CRUD operations for tags and tag assignments.
- Enable filtering prompts by one or more tags while respecting collection filters.

This feature empowers teams to quickly surface prompts for a persona or stage (e.g., `customer-support`, `baseline`, `experimental`).

---

## User Stories

### Story 1: Attach tags when creating or updating a prompt

**As** a prompt engineer
**I want** to include tags during prompt creation and updates
**So that** I can categorize prompts from the outset.

**Acceptance Criteria**
- `PromptCreate` and `PromptUpdate` payloads accept an optional `tags` list of strings.
- Tags are normalized to lowercase and deduplicated before storing (e.g., `"Baseline"` becomes `"baseline"`).
- Tag strings must be between 1 and 50 characters.

### Story 2: Search prompts by tag combinations

**As** a prompt reviewer
**I want** to filter prompts by one or more tags
**So that** I can view just the prompts relevant to my experiment.

**Acceptance Criteria**
- GET `/prompts?tags=tag1,tag2` returns prompts containing all listed tags (logical AND).
- The tag filter works alongside `collection_id` and `search` parameters.
- Tags are compared case-insensitively but stored in lowercase for consistency.

### Story 3: Manage tag catalog

**As** a team lead
**I want** to list, create, and delete tags
**So that** the catalog stays clean and avoids duplicates.

**Acceptance Criteria**
- GET `/tags` returns the master list of tags with popularity counts.
- POST `/tags` adds a tag if it does not already exist.
- DELETE `/tags/{tag}` removes the tag and disassociates it from any prompts.
- The tag list is sorted alphabetically.

---

## Data Model Design

### Tag (new model)

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Primary key (lowercase) representing the tag text. |
| `created_at` | datetime | When the tag was first seen. |
| `description` | Optional[str] | Optional short explanation (future enhancement). |

### Prompt → Tag relationship

- `Prompt` gains a new field `tags: List[str]` storing normalized tag names.
- The storage layer maintains a mapping of tags to prompt IDs for efficient filtering.
- Deleting a tag removes it from every prompt's `tags` list.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tags` | List all tags with prompt counts. |
| POST | `/tags` | Create a normalized tag. |
| DELETE | `/tags/{tag}` | Delete a tag and remove it from prompts. |
| GET | `/prompts` | Supports `tags` query parameter (comma-separated). |
| POST | `/prompts` | Accepts `tags` field with normalized tag list. |
| PUT | `/prompts/{id}` | Replaces prompt tags along with other fields. |
| PATCH | `/prompts/{id}` | Updates tags while leaving unspecified prompts intact. |

### Example: GET `/tags`

Returns the catalog of tags and how many prompts reference each.

### Example: POST `/tags`

```bash specs/tagging-system.md
curl -X POST http://localhost:8000/tags \
  -H 'Content-Type: application/json' \
  -d '{"name": "experiment"}'
```

### Example: Delete Tag

```bash specs/tagging-system.md
curl -X DELETE http://localhost:8000/tags/experiment
```

### Prompt Filtering by Tags

- `GET /prompts?tags=baseline,executive` returns prompts that include both `baseline` and `executive`.
- Tag filters are combined with `collection_id` and `search` for multi-faceted queries.

---

## Edge Cases

- Tag names that differ only in capitalization (e.g., `Baseline` vs. `baseline`) should collapse into one entry.
- Empty or whitespace-only tags are invalid and should trigger a 400 response.
- Removing a tag via `/tags/{tag}` should not delete prompts; it should only drop the reference from their `tags` list.
- Adding or referencing a tag that does not yet exist should implicitly create it (either during prompt creation or via POST `/tags`).
- Filtering by tags that do not exist should return an empty list rather than an error.
- Unlimited tag lists should be guarded (e.g., maximum 20 tags per prompt) to maintain serialization performance.

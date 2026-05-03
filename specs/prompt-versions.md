# Prompt Versions Feature Specification

## Overview & Goals

PromptLab needs a first-class versioning layer so engineers can track how prompt text evolves, compare changes, and roll back to previous iterations. The versioning feature should:

- Capture immutable snapshots every time a prompt is created or updated.
- Allow retrieval of a prompt's history sorted newest-first.
- Support reverting a prompt to a prior snapshot while preserving the audit trail.

By shipping this feature, teams can conduct experiments with confidence and recover previous wording without fear of accidental overwrites.

---

## User Stories

### Story 1: View prompt history

**As** a prompt engineer
**I want** to see a list of historical versions for each prompt
**So that** I can understand how wording has changed over time.

**Acceptance Criteria**
- GET `/prompts/{id}/versions` returns paginated versions sorted newest-first.
- Each entry includes `version_id`, `created_at`, `title`, `description`, and `collection_id`.
- If a prompt has no history (freshly created), the list contains exactly one entry representing the initial version.

### Story 2: Snapshot on change

**As** a contributor modifying a prompt
**I want** the system to store a new version automatically when I update or patch the prompt
**So that** nothing is lost and I can roll back later.

**Acceptance Criteria**
- Every successful POST, PUT, or PATCH against `/prompts` creates a `PromptVersion` record before the new prompt values replace the old ones.
- Version numbering increments sequentially (1, 2, 3, ...).
- Timestamp includes the moment the change was persisted.

### Story 3: Revert to previous version

**As** a reviewer
**I want** to revert a prompt to an earlier version with a single action
**So that** I can recover wording that was accidentally overwritten in a more recent iteration.

**Acceptance Criteria**
- POST `/prompts/{id}/versions/{version_id}/revert` copies the version's data back to the prompt and creates a new version representing the revert event.
- The revert response returns the prompt's new version metadata.
- Reverting does not delete historical versions.

---

## Data Model Design

### PromptVersion (new model)

| Field | Type | Description |
|-------|------|-------------|
| `version_id` | UUID | Unique identifier for the version snapshot. |
| `prompt_id` | UUID | Foreign key to the parent prompt. |
| `version_number` | int | Sequential version number per prompt. |
| `title` | str | Prompt title at this point in history. |
| `content` | str | Prompt text template. |
| `description` | Optional[str] | Description at the time of the snapshot. |
| `collection_id` | Optional[str] | Collection assignment at that time. |
| `created_at` | datetime | Timestamp when the snapshot was created. |
| `source` | str | Indicator of what triggered the version (`create`, `update`, `patch`, `revert`). |

### Storage Considerations

- `Storage` class gets new dictionaries to track `PromptVersion` records and indexes keyed by `prompt_id`.
- On prompt change, insert a new `PromptVersion` before updating the `Prompt` record.
- Provide helper utilities to fetch versions ordered by `version_number`.

---

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/prompts/{id}/versions` | List all versions for a prompt. |
| GET | `/prompts/{id}/versions/{version_id}` | Retrieve a single version detail. |
| POST | `/prompts/{id}/versions/{version_id}/revert` | Revert the prompt to a specific version. |
| (Internal) | Triggered by POST/PUT/PATCH `/prompts` | Automatically store a version before persisting updates. |

### GET `/prompts/{id}/versions`

- Supports pagination via `limit` and `offset` query params.
- Returns a list of versions with metadata and the `source` field.

### GET `/prompts/{id}/versions/{version_id}`

- Returns the exact snapshot, including content, description, and collection.
- Used by UI to preview historical versions before reverting.

### POST `/prompts/{id}/versions/{version_id}/revert`

- Copies payload from the specified version to the `Prompt` record and stores a new version with source `revert`.
- Returns the updated prompt in the response body for convenience.
- Respects collection validation (collection must exist or be null).

---

## Edge Cases

- If the prompt has never been updated, `/prompts/{id}/versions` should return the creation version only.
- Reverting to the latest version (current state) should be idempotent and return 200 with no change.
- If a referenced version is deleted externally, `/revert` should return 404.
- Version numbers must not reset even if collection assignments change; they must remain strictly increasing.
- Concurrent updates should detect stale versions by checking the latest `updated_at` timestamp before storing a new version (future enhancement).

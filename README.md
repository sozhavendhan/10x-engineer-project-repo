# PromptLab

**Your AI Prompt Engineering Platform**

PromptLab is the centralized backend for managing and iterating on prompt engineering assets. Engineers use it to store prompt templates, annotate them with tags and collections, track version history, and experiment with outputs through a stable FastAPI surface.

---

## Overview

PromptLab helps teams move from scattered notes to production-ready prompt flows by offering:

- **Structured prompt storage** with descriptive metadata and optional collection membership.
- **Version tracking readiness** so you can understand how prompt text changes over time (see `specs/prompt-versions.md`).
- **Tagging and categorization** for organizing prompts by audience, persona, or experiment stage (see `specs/tagging-system.md`).
- **Rich APIs** to list, search, and mutate prompts and collections with built-in validation and sorting utilities.
- **Extensible storage model** that is already split into models, storage, and helpers for future persistence upgrades.

---

## Key Capabilities

- Full CRUD for prompts and collections plus health check endpoints.
- Collection and search filters for the prompt list with newest-first ordering.
- Safe collection deletion that disassociates prompts rather than losing data.
- Google-style docstrings across modules for better generated docs.
- Specs and coding guidance that prepare you for versioning and tagging features.

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- (Optional) Node.js 18+ for the frontend work in Week 4

### Installation & Setup

1. Clone the repository and change into the backend subdirectory.
2. Create an isolated virtual environment and install the required dependencies.
3. Run the FastAPI server locally using Uvicorn.

```bash README.md
git clone <your-repo-url>
cd promptlab/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` to explore the Swagger UI.

### Running Tests

```bash README.md
cd backend
source .venv/bin/activate
pytest tests/ -v
```

---

## API Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health and version metadata |
| GET | `/prompts` | List prompts (supports `collection_id` and `search`) |
| GET | `/prompts/{id}` | Fetch a prompt by UUID |
| POST | `/prompts` | Create a prompt with metadata and optional collection |
| PUT | `/prompts/{id}` | Replace a prompt (all fields required) |
| PATCH | `/prompts/{id}` | Partially update a prompt |
| DELETE | `/prompts/{id}` | Delete a prompt permanently |
| GET | `/collections` | List all collections |
| GET | `/collections/{id}` | Retrieve one collection by UUID |
| POST | `/collections` | Create a new collection |
| DELETE | `/collections/{id}` | Delete a collection and orphan associated prompts |

---

## Usage Examples

### Create a Prompt

```bash README.md
curl -X POST http://localhost:8000/prompts \
  -H 'Content-Type: application/json' \
  -d '{"title": "Summarize sprint results", "content": "Provide a summary for {{input}}", "description": "Used for executive updates", "collection_id": null}'
```

### Search Prompts by Keyword

```bash README.md
curl "http://localhost:8000/prompts?search=sprint&collection_id=release-updates"
```

### Partially Update a Prompt Description

```bash README.md
curl -X PATCH http://localhost:8000/prompts/{prompt_id} \
  -H 'Content-Type: application/json' \
  -d '{"description": "Sharper tone for investor updates."}'
```

### Delete a Collection Safely

```bash README.md
curl -X DELETE http://localhost:8000/collections/{collection_id}
```

---

## Project Layout

```
promptlab/
├── backend/      # FastAPI app with models, storage, utils, and tests
├── docs/         # API reference documentation (docs/API_REFERENCE.md)
├── specs/        # Feature specifications (prompt-versions, tagging-system)
└── .github/       # AI agent instructions and future workflows
```

---

## Development Notes

- Update docstrings in `app/models.py`, `app/api.py`, `app/storage.py`, and `app/utils.py` whenever behavior changes.
- Reuse `storage` helpers instead of manipulating dictionaries to keep logic centralized.
- Follow the specs under `specs/` before adding features so requirements stay aligned.

---

## Documentation & References

- **API Reference**: `docs/API_REFERENCE.md` (request/response samples, error codes).
- **AI Agent Guidance**: `.github/copilot-instructions.md` (coding standards, naming, patterns).
- **Feature Specs**: `specs/prompt-versions.md` and `specs/tagging-system.md` for upcoming work.

---

## Need Help?

1. Visit `http://localhost:8000/docs` for live OpenAPI documentation.
2. Read `PROJECT_BRIEF.md` for weekly milestones and deliverables.
3. Consult `GRADING_RUBRIC.md` to understand scoring expectations.
4. Ask questions in the course forum or collaborate with your AI pair programmer.

---

Good luck — ship something you are proud of! 🚀


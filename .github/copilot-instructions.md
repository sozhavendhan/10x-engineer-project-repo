# PromptLab AI Agent Instructions

These guidelines help AI coding assistants align with PromptLab's current standards.

## Coding Standards

- Prioritize clarity and readability in all Python code. Favor expressive variable names and keep functions under ~30 lines when possible.
- Document every new function and class with **Google-style docstrings** including Args, Returns, and Raises when applicable.
- Keep dependencies minimal; rely on the standard library unless a third-party package is already listed in `backend/requirements.txt`.
- Maintain consistent formatting (PEP 8) and avoid trailing whitespace or unused imports.

## Naming Conventions

- Use `snake_case` for functions, methods, and variables.
- Use `CamelCase` for Pydantic models or dataclasses.
- Prefix private helpers with an underscore if they are not part of the public API.
- Be explicit: prefer names like `prompt_id` instead of `pid` and `validate_prompt_content` instead of `validate`.

## Architecture Guidelines

- Core business logic lives in `backend/app/api.py`, `backend/app/storage.py`, and `backend/app/utils.py`. Keep the FastAPI routes lean; delegate validation and transformation to helpers or storage methods.
- Storage is currently in-memory. Avoid adding persistence-related complexity unless you're implementing a new storage backend (`JSONFileStorage`, `SQLiteStorage`, etc.).
- Introduce new endpoints only after updating the API reference (`docs/API_REFERENCE.md`) and the README sections describing those endpoints.
- When modifying models, update docstrings, type hints, and serializers so downstream docs and tests stay accurate.

## Prompt Patterns for AI Help

Use these prompts when requesting AI-generated code or explanations:

1. **Adding a new endpoint**
   - "Generate a FastAPI POST endpoint for PromptLab that stores prompt version metadata and returns the new version record. Follow the existing validation patterns and update `docs/API_REFERENCE.md`."

2. **Writing helper logic**
   - "Create a utility that filters prompts by tag list and respects case insensitivity. Reference existing helpers in `app/utils.py`."

3. **Documenting behavior**
   - "Provide a Google-style docstring for this storage method explaining when it returns `None` vs. a record."

4. **Testing**
   - "Write a pytest function that verifies filtering prompts by collection works even if the collection is deleted. Use the storage fixture from `tests/conftest.py`."

Always double-check generated code against the existing module style and test suite before merging.

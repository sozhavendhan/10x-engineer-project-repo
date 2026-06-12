# Production Readiness Guide

This document describes what to do before running PromptLab in a production or staging environment.

---

## 1. Prerequisites

| Tool | Minimum version |
|------|----------------|
| Python | 3.11 |
| Docker | 24.x |
| Docker Compose | v2 |

---

## 2. Environment Configuration

Copy `.env.example` to `.env` and update every variable.

```bash
cp .env.example .env
```

Key changes for production:

| Variable | Development default | Production recommendation |
|----------|--------------------|-----------------------------|
| `APP_ENV` | `development` | `production` |
| `APP_RELOAD` | `true` | `false` |
| `CORS_ORIGINS` | `*` | Specific domain(s) e.g. `https://app.example.com` |
| `LOG_LEVEL` | `INFO` | `WARNING` or `ERROR` |

---

## 3. Running with Docker

### Build and start

```bash
docker compose up --build -d
```

### Verify the service is healthy

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "healthy", "version": "0.1.0"}
```

### Stop

```bash
docker compose down
```

---

## 4. Running Tests Before Deploy

Always run the full test suite and verify coverage before shipping.

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v --cov=app --cov-report=term-missing --cov-fail-under=80
```

The CI pipeline (`.github/workflows/ci.yml`) enforces an 80 % coverage floor automatically on every push.

---

## 5. Persistent Storage

The current storage layer is **in-memory only**. All data is lost when the process restarts.

To add persistence, implement a new backend in `backend/app/storage.py` that satisfies the same interface (e.g. `JSONFileStorage` or `SQLiteStorage`). The `Storage` class methods are documented with Google-style docstrings to guide any replacement.

---

## 6. Horizontal Scaling Considerations

Because storage is in-memory, running multiple instances will produce split state. Before scaling horizontally:

1. Replace the in-memory store with a shared data store (Redis, PostgreSQL, etc.).
2. Remove the volume mount in `docker-compose.yml` (only needed for live-reload in development).
3. Set `--workers N` on the Uvicorn command to match the number of CPU cores.

---

## 7. Security Checklist

- [ ] Set `CORS_ORIGINS` to your actual frontend domain, not `*`.
- [ ] Run behind a reverse proxy (nginx or a cloud load balancer) that terminates TLS.
- [ ] Add authentication middleware before exposing the API publicly.
- [ ] Pin dependency versions in `requirements.txt` and audit with `pip-audit`.
- [ ] Rotate secrets and API keys before each production release.

---

## 8. Health Check

The `/health` endpoint is available for load-balancer probes and uptime monitors.

```
GET /health → 200 {"status": "healthy", "version": "0.1.0"}
```

Docker Compose is already configured to probe this endpoint every 30 seconds.

---

## 9. API Documentation

Interactive Swagger UI is served at `/docs` and ReDoc at `/redoc` by FastAPI automatically. Disable these in production if the API should not be publicly browsable:

```python
app = FastAPI(docs_url=None, redoc_url=None)
```

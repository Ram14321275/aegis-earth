# Aegis Earth Backend

Official Sprint 1 backend workspace.

## Structure

```text
backend/
  requirements.txt
  pytest.ini
  app/
    api/v1/       Versioned API routes
    core/         Settings, logging, and security helpers
    models/       Domain models, database integration deferred
    schemas/      Pydantic schemas
    services/     Backend application services
    utils/        Shared utilities
    validators/   Request and domain validation
    middleware/   Request and response middleware
    tests/        Backend tests
    main.py       FastAPI application entrypoint
```

Keep backend implementation aligned with the service boundaries in `services/`.

## Checkpoint 3

Run locally:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Health endpoint:

```text
GET /api/v1/health
```

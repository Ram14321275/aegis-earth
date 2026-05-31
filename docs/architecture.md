# Architecture

## System Overview

Aegis Earth is organized around clean service boundaries so disaster intelligence can grow without coupling UI, API, model, cache, alert, and visualization concerns.

```text
frontend/ React operator console
backend/  FastAPI application
services/
  disaster-engine/
  model-interface/
  cache/
  alert-engine/
  visualization/
  geospatial/
docs/
  decisions/
```

## Repository Workspaces

- `frontend/src/features`: MVP feature modules for location search, flood intelligence, wildfire intelligence, map evidence, alerts, and explainability.
- `frontend/src/store`: client-side state management for MVP workflows.
- `backend/app/api/v1`: versioned FastAPI route ownership.
- `backend/app/validators`: request and domain validation.
- `backend/app/middleware`: request/response middleware.
- `backend/app/tests`: backend verification.
- `docs/decisions`: approved architecture decision records.

## Frontend

The frontend is an operator-facing mission-control interface. It prioritizes visual evidence and explains why an area is dangerous through:

- Operational map view
- Heat map view
- Difference map view
- Risk assessment
- Confidence indicators
- Alert summaries
- Explainability panel

## Backend

The FastAPI backend exposes versioned API routes under `/api/v1`.

Sprint 1 Checkpoint 3 establishes the backend foundation under `backend/app`:

```text
backend/app/
  api/v1/       Versioned API routes
  core/         Settings, structured logging, and security helpers
  middleware/   Request context and security header middleware
  models/       Domain models, with database integration deferred
  schemas/      Pydantic request and response schemas (with unified APIResponse envelope)
                - geospatial.py: Coordinate and location abstractions
                - intelligence.py: Disaster analysis response contracts
  services/     Backend application services
  utils/        Shared backend utilities
  validators/   Input validation primitives
  tests/        Backend tests
  main.py       FastAPI application entrypoint
```

Current API foundation:

- `GET /api/v1/health`
- Unified `{"data": ..., "error": ...}` API response envelope for all endpoints
- Context-bound `request_id` structured JSON logging for observability
- Global exception handlers catching validation and unhandled exceptions securely
- Pydantic Settings configuration
- Explicit CORS origin configuration prepared for future frontend integration
- Security response headers through middleware
- No database integration yet
- No Google Earth Engine or Sentinel integration yet

Future disaster intelligence request flow:

1. Accept city or latitude/longitude search.
2. Resolve search into coordinates.
3. Check cache.
4. Run disaster engine analysis.
5. Generate alerts and evidence layer descriptors.
6. Return explainable intelligence response.

## Service Boundaries

- `disaster-engine`: flood and wildfire scoring, risk assessment, explainable drivers.
- `model-interface`: stable contracts for future model replacement.
- `cache`: cache-first strategy and request deduplication primitives.
- `alert-engine`: alert generation from hazard signals.
- `visualization`: map, heat map, and difference map layer descriptors.
- `geospatial`: coordinate resolution and geospatial normalization.

## Performance Strategy

- Cache-first analysis endpoint.
- Request key normalization by rounded coordinates.
- Lazy frontend map rendering.
- Background scheduler reserved for provider ingestion and cache warming.

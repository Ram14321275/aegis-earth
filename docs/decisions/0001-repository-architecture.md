# 0001 - Repository Architecture

## Status

Approved

## Context

Aegis Earth needs clear frontend, backend, documentation, infrastructure, script, and service boundaries during Sprint 1.

## Decision

The repository uses these MVP workspaces:

- `frontend/` for the React operator interface.
- `backend/` for the FastAPI application structure.
- `services/` for disaster intelligence service ownership boundaries.
- `docs/` for sprint, architecture, API, database, security, and decision documentation.
- `infrastructure/` for MVP deployment and environment assets.
- `scripts/` for development workflow scripts.

Backend application code is organized under `backend/app` with:

- `api/v1` for versioned API routes.
- `validators` for request and domain validation.
- `middleware` for request/response middleware.
- `tests` for backend tests.

Frontend application code is organized under `frontend/src` with:

- `features` for MVP feature modules.
- `store` for client state management.

## Consequences

- New implementation should prefer the approved `frontend/` and `backend/` workspaces.
- No non-MVP feature folders should be added during Sprint 1.
- Existing service boundaries remain separate so future models can be replaced through `model-interface`.


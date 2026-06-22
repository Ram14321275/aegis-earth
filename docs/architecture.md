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
- `POST /api/v1/search` (Search orchestration layer)
- Unified `{"data": ..., "error": ...}` API response envelope for all endpoints
- Context-bound `request_id` structured JSON logging for observability
- Global exception handlers catching validation and unhandled exceptions securely
- Pydantic Settings configuration
- Explicit CORS origin configuration prepared for future frontend integration
- Security response headers through middleware
- No database integration yet
- No Google Earth Engine or Sentinel integration yet

Future disaster intelligence request flow:

1. Accept `POST /api/v1/search` with city query or latitude/longitude.
2. `SearchService` orchestrates resolution and computes a versioned cache key.
3. `CacheService` lookup (if hit, return immediately).
4. `GeospatialService` resolves search into coordinates or reverse-geocodes.
5. `AnalysisService` runs disaster engine analysis (currently mocked).
6. Generate alerts and evidence layer descriptors.
7. `CacheService` stores the generated `AnalysisResult` in Redis.
8. Return `AnalysisResult` via `APIResponse`.

## Service Boundaries

- `search`: entrypoint orchestrator bridging requests to domains.
- `cache`: TTL-based Redis distributed cache mapping versioned tile keys to intelligence responses, protected by distributed locks.
- `analysis`: high-level disaster analysis orchestration.
- `disaster-engine`: flood and wildfire scoring, risk assessment, explainable drivers.
- `core/analysis/flood`: deterministic flood intelligence engine utilizing Earth Engine.
- `core/analysis/wildfire`: deterministic wildfire intelligence engine utilizing Earth Engine.
- `core/analysis/change_detection`: historical multi-timeframe environmental intelligence engine tracking vegetation, water, urban, and burn changes.
- `core/intelligence`: Unified planetary intelligence orchestration layer handling cross-hazard correlation, AI explainability generation, and event prioritization.
- `core/streaming`: Real-Time Intelligence Streaming Layer bridging internal Pub/Sub events safely to connected WebSocket Gateways with backpressure and subscription limits.
- `model-interface`: stable contracts for future model replacement.
- `domain`: Earth observation domain model standardizing hazards and risk scoring logic independent of specific models or APIs.
- `core/alerts`: Alert intelligence layer generating deterministic situational alerts driven by risk categorization.
- `core/visualization`: Visualization data layer dynamically compiling overlays, heatmaps, and GeoJSON structures for Leaflet integration.
- `db`: Database foundation handling async operations with explicit Repository patterns supporting Location, Analysis, Risk, Alerts, and Audit logs.
- `frontend`: React frontend application deployed using Vite, mapped explicitly with Leaflet bounds and dynamic Intelligence Dashboard layouts including Search Experience tracking local state telemetry, Dashboard KPI modules, Alert Feeds, and Risk Summaries.
- `core`: Infrastructure code including configuration, logging, and security.
- `core/cache`: Unified Redis caching foundation handling request deduplication via distributed locks, TTL evictions, and metrics synchronization.
- `core/jobs`: Analysis Job domain tracking spatial computations through strict state machines, enabling asynchronous workloads decoupled from HTTP request loops.
- `core/workers`: Background Worker Architecture bound to the FastAPI lifecycle, processing queued jobs robustly with automatic retry recovery and offline purges via the Scheduler.
- `core/risk`: Standardized risk engine scoring hazards dynamically through threshold-driven rule configurations.
- `observability`: Core telemetry, metrics, and health aggregation tracking system state.
- `geospatial`: App boundary for robust PostGIS operations via GeoAlchemy2. Handles bounds checking, distance geometry calculations, and strict WKT casting decoupled from specific models.
- `db`: Database foundation handling async operations with explicit Repository patterns supporting Location, Analysis, Risk, Alerts, and Audit logs.
- `satellite`: Core abstraction layer bounding all external Satellite Imagery requests (e.g. Sentinel, Earth Engine). Integrates robust Registry mapping, bounding validators, and deterministic Mock providers shielded directly by Redis caching schemas.
  - `integrations/gee`: Standalone module injecting the `GoogleEarthEngineProvider` via ThreadPool offloading mapping Sentinel 1/2 imagery natively into AEGIS formats, protected by `tenacity` retry logic and an active `CircuitBreaker`.
- `alert-engine`: alert generation from hazard signals.
- `visualization`: map, heat map, and difference map layer descriptors.
- `geospatial`: coordinate resolution and geospatial normalization.

## Performance Strategy

- Cache-first analysis endpoint.
- Request key normalization by rounded coordinates.
- Lazy frontend map rendering.
- Background scheduler reserved for provider ingestion and cache warming.

## Security & Multi-Tenancy Architecture
- **TenantAwareModel**: Enforces global tenant_id partitioning via BaseRepository.
- **AuthenticationMiddleware**: Decouples auth completely from hazard engines using PyJWT.
- **RBAC**: Policy-driven role mappings managed internally via contextvars.

## Distributed Processing Architecture
- **Job Orchestration**: Asynchronous execution via `app/core/jobs/orchestration.py`, resolving APIs to `202 Accepted`.
- **Deduplication Engine**: Redis `SET NX EX` atomic locking mechanism via request fingerprint hashes (`coordinates|timeframe|hazard_type|versions`).
- **Idempotency**: Natively resolves `Idempotency-Key` headers to prevent mobile/unstable network retry duplications.
- **Worker Isolation**: Stateless, async, horizontally scalable workers executing leases with 10-minute timeout enforcement and internal credential validation.
- **Priority Scheduler**: Queue priorities defined algebraically via weighted severity, population risk, tenant tier SLA, and request urgency heuristics.

## Planetary Intelligence Coordination (Fusion Layer)
- **Disaster Fusion Engine**: Combines isolated hazards into a unified `RegionalThreatAssessment` utilizing bounded spatial clustering and compound risk amplifiers.
- **Temporal Consistency Engine**: Mitigates volatile threshold oscillations via independent escalation/de-escalation hysteresis tracking and time-decay weighting.
- **Reliability Validation**: Calculates explicit confidence bounds without mutating underlying analytical results, penalizing high cloud coverage and provider degradation.
- **Correlation & Cascading Analysis**: Identifies inter-hazard causal loops (e.g. wildfire scars increasing flood vulnerability) bound strictly by region and temporal cooldown rules.
- **Operational Prioritization**: Calculates global urgency dynamically factoring active worker queue saturation, avoiding non-critical escalations during planetary-scale system congestion.
- **Anomaly Protection**: Deterministically suppresses impossible intelligence jumps and sudden confidence collapses, guaranteeing operational stability.

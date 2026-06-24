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

## Global Intelligence API Gateway & Federation
- **Unified Query API**: Centralized endpoint (`POST /api/v1/intelligence/query`) abstracting all internal engines via `gateway/router.py`.
- **Request Coalescer**: Thundering herd protection via Redis. Identical in-flight requests are fingerprinted (`tenant+payload+version`), locked, and multiplexed from a single background execution.
- **Federation Engine**: `asyncio.gather()` orchestration with strict per-engine timeouts and partial degradation via `CircuitBreaker`. Ensures a single failing hazard engine NEVER fails the entire unified response.
- **Adaptive Cache Policy**: Dynamic TTL scaling driven by hazard severity (e.g., Critical = 10m, Stable = 6h) enforcing fresher data during active crises.
- **Public Contracts**: Strict, versioned schemas (`IntelligenceSnapshot`, `RegionalSummary`) shared equally between REST and WebSocket interfaces.
- **SDK Generation**: Automated extraction of OpenAPI schema utilizing `openapi-generator-cli` to scaffold perfectly typed TypeScript and Python clients.
- **Rate Limiting**: Sliding-window Token Bucket rate limiting via Redis. Supports Tenant, API-Key, and IP level quotas.

## Geospatial Visualization & Tile Streaming Layer
- **PostGIS Mapbox Vector Tiles (MVT)**: Natively generated vector geometries delivered via `ST_AsMVT` and `ST_AsMVTGeom`, eliminating mid-tier payload serialization overhead. Protected by strict `GiST` spatial indexing.
- **Dynamic Level of Detail (LOD)**: Zoom-sensitive `ST_SimplifyPreserveTopology` dynamically trims geometric fidelity on low-zoom planetary overviews to protect frontend render loops.
- **Raster Rendering Stack**: High-throughput rendering pipeline generating `WebP/PNG` heatmap and analytical intensity overlays natively without immediate GPU coupling.
- **Edge Caching Engine**: CDN-aware architecture generating highly tunable `Cache-Control` (`stale-while-revalidate`), `ETag`, and `Vary: X-Tenant-ID` HTTP headers based dynamically on localized hazard severity.
- **Websocket Tile Federation**: Delivers highly scoped viewport invalidation (`tile_invalidation`) events to connected `Stitch` frontends, triggering lazy re-fetches without massive broadcast storms.
- **Visualization Contracts**: Stable `LayerManifest` and `TileMetadata` JSON contracts isolating external rendering libraries (Mapbox GL, Leaflet) from volatile internal backend representations.

## Planetary Command Center & Timeline Layer
- **Global Timeline Engine**: Pre-materializes short-term (1h, 24h, 7d) operational windows while supporting dynamic streaming aggregations for custom macro-ranges.
- **Threat Prioritization Ranking**: A fully explainable, deterministic engine applying strict weights against raw severity, confidence, population exposure, cross-hazard fusion amplification, and historical persistence.
- **Immutable Snapshot Persistence**: Ensures all timeline frames are captured as append-only immutable records (`TimelineSnapshot`), guaranteeing export and audit consistency during rapidly changing planetary events.
- **Async Export Engine**: Dispatches JSON, CSV, and GeoJSON report generation directly into the Redis-backed worker layer, averting HTTP timeouts and shielding active hazard engines from expensive I/O scans.
- **Command Center WebSocket Streams**: Granular, backpressure-safe channels (`/ws/command-center`) distributing explicit `ESCALATION_WARNING` and priority shifts instantaneously to connected enterprise dashboards.

## Autonomous Predictive Intelligence Layer
- **Hazard Forecasting**: Employs adaptive TTLs and statistical baselines to project temporal escalations. Guarantees 100% deterministic fallback capabilities and strictly penalizes confidence based on telemetry staleness.
- **Infrastructure Prediction**: Actively monitors queue depth, worker saturation, and streaming throughput via the `MetricsStore` to predict overload events before they trigger system cascading failures.
- **Autonomous Remediation**: Translates infrastructure forecasts into safe, explainable `RemediationPlans`. For safety, destructive actions (e.g., node termination) are barred without strict human override, though safe scale-out actions can be recommended.
- **Anomaly Detection**: Scans multi-region streams for telemetry drift and hazard spikes using statistical variance bounds paired with explainable AI signal classifiers.
- **Planetary Simulation**: Conducts extensive `ScenarioSimulation` runs over projected horizons (up to 90 days), calculating cascading impact metrics and population vulnerability trajectories asynchronously.
- **Strict Explainability**: Opaque AI is structurally banned. Every predictive engine conforms to the `Explanation` contract, explicitly detailing contributing sources, weights, uncertainty bounds, and degraded-mode warnings.

## Global AI Copilot & Mission Intelligence Layer
- **Deterministic Narrative Engine**: Replaces opaque LLMs with template-driven logic generating Mission SITREPs, Executive Digests, and Escalation Narratives with absolute reproducibility.
- **Explainability Validation**: Enforces that every emitted narrative retains a cryptographic `reasoning_hash` directly linking back to its underlying evidence. Rejects any orphaned or hallucinated recommendations automatically.
- **Strict Governance Engine**: Pre-evaluates all operational actions. Automatically blocks destructive infrastructure manipulation or autonomous human evacuations, while strictly verifying all recommendation confidence boundaries (e.g. CRITICAL > 0.9).
- **Mission Memory Architecture**: Provides thread-scoped operational persistence leveraging Redis lists with rolling 7-day TTL configurations to isolate tenant mission history safely.
- **WebSocket Federation Expansion**: Integrates high-throughput `/ws/copilot` and `/ws/mission` streaming channels seamlessly through the unified `WebSocketFederationManager`, enabling seamless frontend telemetry updates.

## Global Operations Console & Human Coordination Layer
- **Immutable Investigation History**: Enforces append-only revision trees and cryptographic snapshot linkages for all analyst investigations. Never mutates historical states directly, ensuring comprehensive attribution.
- **WebSocket Safety Model**: Isolates authoritative state within PostgreSQL and Redis event streams. WebSockets are restricted strictly to optimistic UI synchronization and presence broadcasting (`/ws/collaboration`, `/ws/operations`).
- **Deterministic Escalation Engine**: Governs incident escalation logic preventing recursive feedback loops through strict cooldown windows, depth limits, and correlation tracing. Never triggers autonomous destructive actions.
- **Operator Presence & Collaboration**: Synchronizes real-time map positions, annotations, and bookmarks ephemerally using Redis TTLs, automatically evicting stale presences.

## Global External Integrations & Emergency Interoperability Layer
- **Provider Framework Abstraction**: Implements a strict `ProviderInterface` backed by a circuit breaker and health tracking mechanism. Ensures internal orchestration engines remain completely isolated from vendor-specific data models and degradation.
- **Replay-Safe Ingestion Pipeline**: Guarantees deterministic ingestion through strict schema validation and cryptographic payload hashing for deduplication. Malformed payloads are explicitly shunted into dead-letter queues to shield the core intelligence loop.
- **Deterministic Normalization Engine**: Reconciles heterogeneous multi-vendor formats (e.g., CAP, weather feeds) into the immutable `CanonicalHazardEvent`. Operates with strict deterministic severity scaling and confidence adjustment to prevent opaque transformations.
- **Webhook Security Gateway**: Intercepts all inbound vendor webhooks via strict HMAC signature verification, nonce validation, and payload timestamp validation to explicitly thwart replay and impersonation attacks.
- **Explainable Humanitarian Coordination**: Handles external NGO resource and shelter routing requests by applying strict deterministic, explainable prioritization rankings. Completely bans opaque black-box AI from autonomous operational logic.
- **Secure Export Engine**: Transpiles immutable canonical states into standard distribution formats (CAP 1.2, GeoJSON) securely, strictly preserving timeline lineage and confidence while preserving tenant isolation.

## Sovereign Intelligence Governance, Compliance & Forensic Audit Layer
- **Immutable Forensic Audit Engine**: Cryptographically signs and chains every critical operation (escalations, generation, overrides) using `HMAC-SHA256` preserving unbroken `lineage_path`s. Reordering or mutation invalidates the sequence entirely.
- **Deterministic Governance Policies**: Enforces strict operator overrides, sovereign boundary protections, and regional sharing logic synchronously without utilizing opaque black-box AI.
- **Human Approval Workflow Layer**: Halts critical destructive or cross-border operations utilizing an asynchronous multi-party approval state machine. Every decision natively merges into the tamper-proof audit chain.
- **Sovereign Isolation Layer**: Employs string-matching and future `ST_Contains` spatial rules to lock tenant intelligence strictly inside geopolitical bounds, intercepting illegal external deliveries via the `SovereigntyResolver`.
- **Forensic Replay Engine**: Assembles timeline snapshots and historical audit events to recreate EXACT intelligence states deterministically for any historical timestamp, deliberately ignoring live mutable data models.
- **Retention & Compliance Layer**: Facilitates retention logic executing evidence-backed compliance bundle generation. Bypasses naive TTL mechanisms allowing manual and legal-hold archives dynamically.

## Edge Intelligence & Global Synchronization Layer
- **Distributed Topology & Registry**: Manages `EdgeNode` registration, heartbeat monitoring, and sovereign region mapping to partition workloads correctly across global regions.
- **Failover & Redis Elections**: Prevents split-brain deployments by using Redis-backed fencing tokens, lease locking (`SET NX PX`), and strict consensus when promoting standby nodes during outages.
- **Synchronization & Reconciliation Engine**: Synchronizes edge states deterministically. Relies on lineage continuity and strict conflict arbitration (e.g., timestamp comparison) explicitly rejecting lossy operations.
- **Degraded Operation Mode**: Captures operations safely in `OfflineQueueManager` during network partitions, buffering hazard updates locally until reconnection.
- **Verifiable Continuity**: Validates historical event chains (`ConsistencyVerifier`) during synchronization preventing orphaned states from propagating globally.

## Autonomous Cyber Defense & Zero-Trust Security Fabric
- **Deterministic Detection Engine**: Evaluates threat signals (e.g., websocket floods, replay nonces) without opaque ML, yielding explainable reasoning and hashes.
- **Zero-Trust Identity Fabric**: Discards implicit internal trust. Verifies attestation signatures (HMAC), checking monotonic counters and tracking replay nonces globally.
- **Autonomous Containment**: Executes strict, reversible remediation automatically (e.g., rate-limiting, edge partition) while isolating enterprise tenant disruption behind an `ApprovalWorkflowEngine` gate.
- **Forensic Replay & Tamper Traceability**: Links cyber incidents tightly with the governance ledger, rendering attack timelines fully replayable and immutable.

## Autonomous Sovereign Resilience & Self-Healing Infrastructure Mesh
- **Deterministic Healing**: Triggers safe recovery workflows (e.g. `clear_cache`) autonomously while blocking destructive actions like `drop_database` and gating runtime restarts behind the ApprovalWorkflow.
- **Sovereign Failover**: Utilizes Redis-backed fencing tokens to execute failovers safely while enforcing geographic boundaries so a node in US-EAST cannot accidentally failover to EU-WEST.
- **Predictive Stabilization**: Actively monitors queue depth, websocket capacity, and CPU load to issue deterministic stabilization actions before infrastructure collapse.
- **Fail-Closed Lineage Verification**: Every snapshot restoration cryptographically hashes the lineage. Any discontinuity or split-brain corruption instantly aborts recovery.

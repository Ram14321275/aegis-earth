# cache

Owns cache-first response behavior and request deduplication primitives.

Sprint 1 uses an in-memory TTL cache. Later phases can replace this with Redis or a regional cache without changing route contracts.

Runtime implementation currently lives in `apps/api/app/services/cache`.


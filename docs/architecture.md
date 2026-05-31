# Architecture

## System Overview

Aegis Earth is organized around clean service boundaries so disaster intelligence can grow without coupling UI, API, model, cache, alert, and visualization concerns.

```text
apps/
  web/ React operator console
  api/ FastAPI application
services/
  disaster-engine/
  model-interface/
  cache/
  alert-engine/
  visualization/
  geospatial/
```

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

The FastAPI backend exposes versioned API routes under `/api/v1`. Request flow:

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


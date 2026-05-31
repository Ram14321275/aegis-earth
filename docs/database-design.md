# Database Design

## Current Sprint 1 State

PostgreSQL is configured through `DATABASE_URL`, but persistent tables are not created until migrations are introduced.

## Planned MVP Tables

### locations

- `id`
- `name`
- `latitude`
- `longitude`
- `created_at`

### analysis_runs

- `id`
- `location_id`
- `query`
- `overall_risk`
- `confidence`
- `generated_at`
- `metadata`

### disaster_signals

- `id`
- `analysis_run_id`
- `type`
- `risk`
- `confidence`
- `drivers`

### alerts

- `id`
- `analysis_run_id`
- `severity`
- `title`
- `message`
- `created_at`

### evidence_layers

- `id`
- `analysis_run_id`
- `layer_type`
- `label`
- `description`
- `asset_uri`

## Notes

- Use JSONB for provider metadata and signal driver arrays when migrations are added.
- Add geospatial indexing after PostGIS is confirmed for the deployment environment.


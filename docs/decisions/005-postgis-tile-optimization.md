# PostGIS Tile Optimization Strategy

Date: 2026-06-22

## Context
With the introduction of the Global Geospatial Intelligence Visualization & Tile Streaming Layer (Checkpoint 46), Aegis Earth will serve millions of Mapbox Vector Tiles (MVT) generated directly from PostGIS using `ST_AsMVT`. 

To prevent full-table spatial scans and ensure rendering remains performant under high concurrency, strict indexing and partitioning strategies are required.

## Decisions

### 1. Mandatory GiST Indexes
All geometry columns accessed by the tile engine must be indexed using `GiST`.
```sql
CREATE INDEX idx_hazards_geometry ON hazards USING GIST (geometry);
```

### 2. Spatial Bounding Pre-Filters
All tile queries MUST utilize `ST_Intersects` wrapped against a bounding box created by `ST_MakeEnvelope`. This allows the GiST index to rapidly filter out geometries before applying the expensive `ST_SimplifyPreserveTopology` and `ST_AsMVTGeom` functions.
```sql
AND ST_Intersects(h.geometry, ST_Transform(bounds.geom, 4326))
```

### 3. Zoom-Sensitive Geometry Simplification
We utilize a dynamic `tolerance` variable in `ST_SimplifyPreserveTopology(h.geometry, :tolerance)`. The tolerance shrinks as zoom levels increase (approaching zero), discarding microscopic vertex points when rendering global overviews.

### 4. Tenant Isolation
Tenant IDs are strictly evaluated alongside the spatial boundary. A composite index is recommended for highly multi-tenant environments:
```sql
CREATE INDEX idx_hazards_tenant_geom ON hazards USING GIST (geometry) WHERE tenant_id IS NOT NULL;
```

### 5. Future: Geometry Partitioning
As historical archives grow, we will implement PostgreSQL native partitioning by `timeframe` AND `hazard_type` to ensure queries for 'Active Floods' do not scan historical 'Wildfire' tables, even within identical spatial envelopes.

# API Reference

## Authentication
Currently, the MVP relies on internal network boundaries and CORS validation. Public API endpoints are not authenticated in this iteration.

## Endpoints

### `POST /api/v1/search`
Orchestrates the entire intelligence gathering workflow.
- **Request Body**:
  ```json
  {
    "query": "Tokyo",
    "latitude": null,
    "longitude": null
  }
  ```
- **Response**: `AnalysisResult` object containing risk assessment, visual overlays, and active alerts.

### `GET /api/v1/system/health`
Aggregates health across all core subsystems (DB, Cache, Engine).
- **Response**:
  ```json
  {
    "status": "Nominal",
    "components": {
       "database": {"status": "Nominal"}
    }
  }
  ```

### `GET /api/v1/system/metrics`
Exposes the centralized telemetry tracker counts.
- **Response**: `SystemMetricsResponse` tracking average latencies, cache hit ratios, and API requests.

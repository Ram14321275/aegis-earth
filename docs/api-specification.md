# API Specification

Base path: `/api/v1`

## Health

`GET /health`

Response:

```json
{
  "status": "ok",
  "service": "aegis-earth-api"
}
```

## Analyze Location

`POST /api/v1/intelligence/analyze`

Request:

```json
{
  "query": "Hyderabad"
}
```

Request can also use latitude and longitude:

```json
{
  "query": "17.3850,78.4867"
}
```

Response:

```json
{
  "locationName": "Hyderabad",
  "coordinates": {
    "latitude": 17.385,
    "longitude": 78.4867
  },
  "generatedAt": "2026-05-31T00:00:00Z",
  "overallRisk": "high",
  "confidence": 0.82,
  "signals": [
    {
      "type": "flood",
      "risk": "high",
      "confidence": 0.84,
      "drivers": ["Rainfall anomaly sensitivity"]
    }
  ],
  "evidenceLayers": [
    {
      "id": "base-map",
      "label": "Operational Map",
      "type": "map",
      "description": "Coordinate resolved base layer with terrain and urban context."
    }
  ],
  "alerts": [],
  "explanation": []
}
```

## Risk Bands

- `low`
- `moderate`
- `high`
- `critical`


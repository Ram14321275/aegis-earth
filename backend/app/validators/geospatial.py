from fastapi import Query
from app.schemas.geospatial import Coordinates

def validate_search_query(
    query: str = Query(..., min_length=2, max_length=100, description="Search query for location")
) -> str:
    """Validate and sanitize a location search query."""
    sanitized = query.strip()
    return sanitized

def validate_coordinates(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Latitude between -90 and 90"),
    lon: float = Query(..., ge=-180.0, le=180.0, description="Longitude between -180 and 180")
) -> Coordinates:
    """Validate lat/lon query parameters and return a Coordinates schema."""
    return Coordinates(lat=lat, lon=lon)

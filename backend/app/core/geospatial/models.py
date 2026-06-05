from typing import List, Tuple
from pydantic import BaseModel, Field

class Point(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")

class BoundingBox(BaseModel):
    min_lon: float = Field(..., ge=-180, le=180)
    min_lat: float = Field(..., ge=-90, le=90)
    max_lon: float = Field(..., ge=-180, le=180)
    max_lat: float = Field(..., ge=-90, le=90)

class RadiusSearch(BaseModel):
    center: Point
    radius_meters: float = Field(..., gt=0, description="Radius in meters")

class PolygonArea(BaseModel):
    # A polygon is a list of points (lat, lon) or just coordinates. 
    # For GeoJSON and WKT it's usually (lon, lat).
    coordinates: List[Tuple[float, float]] = Field(
        ..., 
        min_length=3, 
        description="List of (lon, lat) tuples forming a closed polygon"
    )

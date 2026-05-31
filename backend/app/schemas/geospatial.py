from typing import Optional
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    lat: float = Field(..., ge=-90.0, le=90.0, description="Latitude between -90 and 90")
    lon: float = Field(..., ge=-180.0, le=180.0, description="Longitude between -180 and 180")


class LocationSearchResponse(BaseModel):
    name: str
    coordinates: Coordinates
    confidence: float = Field(..., ge=0.0, le=1.0)
    bounding_box: Optional[list[float]] = Field(
        None,
        description="[min_lon, min_lat, max_lon, max_lat]",
        min_length=4,
        max_length=4,
    )


class ReverseGeocodeResponse(BaseModel):
    name: str
    country: Optional[str] = None
    region: Optional[str] = None

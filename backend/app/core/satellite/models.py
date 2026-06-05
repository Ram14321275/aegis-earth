from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.core.geospatial.models import BoundingBox

class SatelliteMetadata(BaseModel):
    provider: str
    metadata: Dict[str, Any]

class SatelliteScene(BaseModel):
    scene_id: str
    provider: str
    captured_at: datetime
    bbox: BoundingBox
    cloud_cover: float = Field(..., ge=0.0, le=100.0)
    resolution_meters: float
    bands: List[str]
    geometry: str = Field(description="WKT representation of scene boundary")
    metadata: Dict[str, Any]

class SatelliteTimeseries(BaseModel):
    provider: str
    location_wkt: str
    start_time: datetime
    end_time: datetime
    scenes: List[SatelliteScene]

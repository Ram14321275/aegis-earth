from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel


class MapLayer(BaseModel):
    layer_id: str
    layer_url: str
    bounds: List[float]  # [min_lon, min_lat, max_lon, max_lat]


class HeatmapDataPoint(BaseModel):
    lat: float
    lon: float
    intensity: float


class HeatmapLayer(BaseModel):
    layer_id: str
    points: List[HeatmapDataPoint]
    radius: int = 25


class OverlayLayer(BaseModel):
    layer_id: str
    color: str
    polygon: List[List[float]]  # simple polygon


class TimelineEntry(BaseModel):
    timestamp: datetime
    event_type: str  # "RISK_CHANGE", "ALERT_GENERATED", "ANALYSIS_RUN"
    description: str
    metadata: Dict[str, Any]


class GeoJSONGeometry(BaseModel):
    type: str
    coordinates: Any


class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: GeoJSONGeometry
    properties: Dict[str, Any]


class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TileMetadata(BaseModel):
    min_zoom: int = 0
    max_zoom: int = 22
    bounds: List[float] = Field(..., description="[min_lon, min_lat, max_lon, max_lat]", min_length=4, max_length=4)
    attribution: str

class OverlayLegendItem(BaseModel):
    label: str
    color: str
    value: Optional[float] = None

class OverlayLegend(BaseModel):
    title: str
    items: List[OverlayLegendItem]
    type: str = "gradient" # gradient, categorical

class HazardLayerConfig(BaseModel):
    hazard_type: str
    vector_tile_url: str
    raster_tile_url: Optional[str] = None
    legend: OverlayLegend
    metadata: TileMetadata

class VisualizationThemeConfig(BaseModel):
    base_map_style: str
    primary_color: str
    critical_color: str
    warning_color: str

class TemporalLayer(BaseModel):
    start_time: str
    end_time: str
    playback_url: str

class PlaybackFrame(BaseModel):
    timestamp: str
    layer_url: str
    severity_index: float

class HeatmapMetadata(BaseModel):
    hazard_type: str
    z: int
    x: int
    y: int
    max_intensity: float
    data_points: List[Dict[str, Any]]

class LiveTileEvent(BaseModel):
    type: str = "tile_invalidation"
    layer: str
    z: int
    x: int
    y: int
    reason: str
    tile_version: str
    layer_version: Optional[str] = None

class LayerManifest(BaseModel):
    """
    Root manifest describing all available visualizations for a given viewport or tenant.
    """
    version: str = "1.0"
    theme: VisualizationThemeConfig
    hazards: List[HazardLayerConfig]
    temporal: Optional[TemporalLayer] = None

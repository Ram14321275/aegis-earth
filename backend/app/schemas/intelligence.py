from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field

from app.schemas.geospatial import Coordinates


class SeverityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class HazardTypeEnum(str, Enum):
    FLOOD = "flood"
    WILDFIRE = "wildfire"
    # Future scope hazards
    CYCLONE = "cyclone"
    LANDSLIDE = "landslide"
    DROUGHT = "drought"
    VEGETATION_LOSS = "vegetation_loss"
    URBAN_EXPANSION = "urban_expansion"
    UNKNOWN = "unknown"


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BaseIntelligenceModel(BaseModel):
    """Base model enforcing consistency across all disaster analysis outputs."""

    source: list[str] = Field(..., description="Data sources used (e.g., 'Sentinel-2', 'USGS')")
    generated_at: datetime = Field(
        default_factory=get_utc_now, description="Time of generation in UTC"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level 0-1")
    severity: SeverityEnum = Field(..., description="Assessed severity")
    analysis_version: str = Field(..., description="Version of the analysis engine used")
    prediction: Optional[dict[str, Any]] = Field(
        default=None, description="Future prediction placeholder"
    )
    metadata: dict[str, Any] = Field(default_factory=dict, description="Extensibility field")


class RiskAssessment(BaseIntelligenceModel):
    hazard_type: HazardTypeEnum = Field(..., description="Type of hazard")
    score: float = Field(..., ge=0.0, le=100.0, description="Risk score 0-100")
    drivers: list[str] = Field(default_factory=list, description="Key factors driving the risk score")


class MapView(BaseIntelligenceModel):
    type: Literal["map"] = "map"
    layer_url: str = Field(..., description="URL to map tile layer or GeoJSON")
    opacity: float = Field(default=1.0, ge=0.0, le=1.0)
    bounds: list[float] = Field(
        ..., description="[min_lon, min_lat, max_lon, max_lat]", min_length=4, max_length=4
    )


class HeatMapView(BaseIntelligenceModel):
    type: Literal["heatmap"] = "heatmap"
    data_url: str = Field(..., description="URL to heatmap point data")
    intensity_gradient: dict[str, str] = Field(
        default_factory=dict, description="Gradient mapping"
    )
    bounds: list[float] = Field(
        ..., description="[min_lon, min_lat, max_lon, max_lat]", min_length=4, max_length=4
    )


class DifferenceMapView(BaseIntelligenceModel):
    type: Literal["difference"] = "difference"
    before_layer_url: str = Field(..., description="Pre-event imagery layer URL")
    after_layer_url: str = Field(..., description="Post-event imagery layer URL")
    bounds: list[float] = Field(
        ..., description="[min_lon, min_lat, max_lon, max_lat]", min_length=4, max_length=4
    )


class AlertResponse(BaseIntelligenceModel):
    alert_id: str = Field(..., description="Unique alert identifier")
    message: str = Field(..., description="Alert message body")
    recommended_action: Optional[str] = Field(default=None, description="Recommended user action")


class AnalysisResult(BaseIntelligenceModel):
    location_name: str
    coordinates: Coordinates
    risk_assessment: RiskAssessment
    visualizations: list[Union[MapView, HeatMapView, DifferenceMapView]] = Field(default_factory=list)
    alerts: list[AlertResponse] = Field(default_factory=list)

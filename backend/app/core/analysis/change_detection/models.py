from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.intelligence import BaseIntelligenceModel
from app.core.processing.models import AnalysisReadyDataset


class ChangeWindow(str, Enum):
    DAYS_7 = "7d"
    DAYS_30 = "30d"
    DAYS_90 = "90d"
    YEAR_1 = "1y"
    CUSTOM = "custom"


class EnvironmentalRiskCategory(str, Enum):
    STABLE = "STABLE"
    MODERATE_CHANGE = "MODERATE_CHANGE"
    HIGH_CHANGE = "HIGH_CHANGE"
    CRITICAL_CHANGE = "CRITICAL_CHANGE"


class ChangeDirection(str, Enum):
    LOSS = "LOSS"
    GAIN = "GAIN"
    STABLE = "STABLE"
    MIXED = "MIXED"


class ChangeType(str, Enum):
    VEGETATION = "VEGETATION"
    WATER = "WATER"
    BURN = "BURN"
    URBAN = "URBAN"


class TemporalScene(BaseModel):
    window: ChangeWindow
    timestamp: datetime
    ard: AnalysisReadyDataset
    offset_days: int


class SpectralDelta(BaseModel):
    mean_delta: float
    max_loss: float
    max_gain: float
    direction: ChangeDirection
    significant_change_area_km2: float


class ChangeMetrics(BaseModel):
    ndvi_delta: SpectralDelta
    ndwi_delta: SpectralDelta
    nbr_delta: SpectralDelta
    ndbi_delta: SpectralDelta
    cloud_cover_variance: float


class ChangePolygon(BaseModel):
    id: str
    geometry_geojson: Dict[str, Any]
    area_km2: float
    change_type: ChangeType
    direction: ChangeDirection
    timeframe: str
    confidence: float
    generated_at: datetime
    source_scene_ids: List[str]


class ChangeAssessment(BaseIntelligenceModel):
    assessment_id: str
    location_id: Optional[str] = None
    window: ChangeWindow
    risk_score: float = Field(ge=0.0, le=100.0)
    category: EnvironmentalRiskCategory
    metrics: ChangeMetrics
    polygons: List[ChangePolygon]


class EnvironmentalChangeResult(BaseModel):
    assessment: ChangeAssessment
    alertable: bool
    processing_duration_ms: float

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from app.core.processing.models import AnalysisReadyDataset

class BurnSeverityLevel(str, Enum):
    UNBURNED = "UNBURNED"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    EXTREME = "EXTREME"

class WildfireRiskScore(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class BurnPolygon(BaseModel):
    id: str
    geometry_geojson: Dict[str, Any]
    area_km2: float
    severity_level: BurnSeverityLevel

class VegetationImpact(BaseModel):
    baseline_ndvi: float
    current_ndvi: float
    vegetation_loss_percentage: float
    affected_area_km2: float

class WildfireMetrics(BaseModel):
    total_burn_area_km2: float
    high_extreme_burn_area_km2: float
    vegetation_impact: VegetationImpact
    cloud_cover_percent: float = 0.0

class WildfireAnalysisInput(BaseModel):
    current_ard: AnalysisReadyDataset
    baseline_ard: Optional[AnalysisReadyDataset] = None

class WildfireAssessment(BaseModel):
    assessment_id: str
    location_id: Optional[str] = None
    burned_area_km2: float
    confidence: float
    severity: WildfireRiskScore
    metrics: WildfireMetrics
    polygons: List[BurnPolygon] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class WildfireAnalysisResult(BaseModel):
    assessment: WildfireAssessment

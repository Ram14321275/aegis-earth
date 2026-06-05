from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from app.core.processing.models import AnalysisReadyDataset

class FloodRiskScore(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class FloodMetrics(BaseModel):
    baseline_water_area_km2: float
    current_water_area_km2: float
    newly_inundated_area_km2: float
    percentage_increase: float
    flood_growth_factor: float
    cloud_cover_percent: float = 0.0

class FloodPolygon(BaseModel):
    id: str
    geometry_geojson: Dict[str, Any]
    area_km2: float
    is_new_inundation: bool

class FloodAnalysisInput(BaseModel):
    current_ard: AnalysisReadyDataset
    baseline_ard: Optional[AnalysisReadyDataset] = None

class FloodAssessment(BaseModel):
    assessment_id: str
    location_id: Optional[str] = None
    flooded_area_km2: float
    confidence: float
    severity: FloodRiskScore
    metrics: FloodMetrics
    polygons: List[FloodPolygon] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

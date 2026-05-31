from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.intelligence import AnalysisResult


class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskFactors(BaseModel):
    water_coverage: Optional[float] = None
    growth_rate: Optional[float] = None
    burn_area: Optional[float] = None
    spread_rate: Optional[float] = None


class RiskScore(BaseModel):
    numerical_score: float
    level: RiskLevel
    explanation: str


class RiskSummary(BaseModel):
    hazard_type: str
    overall_score: RiskScore
    contributing_factors: List[str]
    confidence_score: float


class RiskAssessmentInput(BaseModel):
    confidence_score: float
    location_metadata: dict
    analysis_result: AnalysisResult

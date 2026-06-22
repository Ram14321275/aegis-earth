import enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.core.predictive.explainability.contracts import Explanation

class ForecastWindow(str, enum.Enum):
    ONE_HOUR = "1h"
    SIX_HOURS = "6h"
    TWENTY_FOUR_HOURS = "24h"
    SEVENTY_TWO_HOURS = "72h"
    SEVEN_DAYS = "7d"
    THIRTY_DAYS = "30d"

class PredictionConfidence(str, enum.Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"

class HazardForecast(BaseModel):
    forecast_id: str
    hazard_type: str
    region_id: str
    predicted_severity: float
    predicted_probability: float
    confidence: PredictionConfidence
    forecast_window: ForecastWindow
    generated_at: datetime
    expires_at: datetime
    explainability: Explanation
    uncertainty_score: float

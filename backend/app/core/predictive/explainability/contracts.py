from pydantic import BaseModel
from typing import List, Optional

class ContributingSignal(BaseModel):
    source: str
    weight: float
    impact: str
    timestamp: str

class Explanation(BaseModel):
    contributing_factors: List[ContributingSignal]
    weighted_reasoning: str
    confidence_explanation: str
    uncertainty_explanation: str
    degraded_mode_active: bool

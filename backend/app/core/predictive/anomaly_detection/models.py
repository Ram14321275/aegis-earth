import enum
from pydantic import BaseModel
from datetime import datetime
from app.core.predictive.explainability.contracts import Explanation

class AnomalyType(str, enum.Enum):
    HAZARD_SPIKE = "HAZARD_SPIKE"
    IMPOSSIBLE_OSCILLATION = "IMPOSSIBLE_OSCILLATION"
    TELEMETRY_DRIFT = "TELEMETRY_DRIFT"
    PROVIDER_INCONSISTENCY = "PROVIDER_INCONSISTENCY"
    TENANT_ABUSE = "TENANT_ABUSE"
    INFRASTRUCTURE_PATTERN = "INFRASTRUCTURE_PATTERN"

class AnomalySignal(BaseModel):
    anomaly_id: str
    detected_at: datetime
    anomaly_type: AnomalyType
    target_entity: str # e.g., "provider_a", "region_x"
    severity: float # 0.0 to 1.0
    is_ai_assisted: bool
    explainability: Explanation

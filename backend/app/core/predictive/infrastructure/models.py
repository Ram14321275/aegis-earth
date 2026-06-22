from pydantic import BaseModel
from app.core.predictive.explainability.contracts import Explanation

class QueuePressureForecast(BaseModel):
    queue_name: str
    saturation_risk: float
    predicted_depth: int
    time_to_saturation_minutes: int

class WorkerCapacityPrediction(BaseModel):
    worker_pool: str
    exhaustion_probability: float
    recommended_scale_up_instances: int

class RegionalLoadPrediction(BaseModel):
    region_id: str
    api_overload_probability: float
    websocket_pressure: float

class InfrastructureForecast(BaseModel):
    forecast_id: str
    overall_health_risk: float
    redis_latency_projection_ms: float
    provider_degradation_probability: float
    queue_forecasts: list[QueuePressureForecast]
    worker_forecasts: list[WorkerCapacityPrediction]
    regional_loads: list[RegionalLoadPrediction]
    explainability: Explanation

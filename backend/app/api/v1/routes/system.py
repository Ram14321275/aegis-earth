from fastapi import APIRouter

from app.observability.health import HealthAggregator
from app.observability.metrics import metrics_store
from app.schemas.common import APIResponse
from app.schemas.observability import SystemHealthResponse, SystemMetricsResponse

router = APIRouter()


@router.get("/metrics", response_model=APIResponse[SystemMetricsResponse])
def get_metrics() -> APIResponse[SystemMetricsResponse]:
    metrics = metrics_store.get_metrics()
    return APIResponse(data=metrics)


@router.get("/health", response_model=APIResponse[SystemHealthResponse])
async def get_health() -> APIResponse[SystemHealthResponse]:
    health_data = await HealthAggregator.get_system_health()
    return APIResponse(data=health_data)

from fastapi import APIRouter, Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.observability.health import HealthAggregator
from app.observability.metrics import metrics_store
from app.schemas.common import APIResponse
from app.schemas.observability import SystemHealthResponse, SystemMetricsResponse

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/metrics")
def get_metrics(request: Request) -> Response:
    if "text/plain" in request.headers.get("accept", ""):
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    
    metrics = metrics_store.get_metrics()
    return APIResponse(data=metrics)


@router.get("/health", response_model=APIResponse[SystemHealthResponse])
async def get_health() -> APIResponse[SystemHealthResponse]:
    health_data = await HealthAggregator.get_system_health()
    return APIResponse(data=health_data)

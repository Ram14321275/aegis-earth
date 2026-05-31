from fastapi import APIRouter

from app.schemas.common import APIResponse
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=APIResponse[HealthResponse])
def health() -> APIResponse[HealthResponse]:
    return APIResponse(data=HealthResponse(status="healthy", service="Aegis Earth", version="v1"))


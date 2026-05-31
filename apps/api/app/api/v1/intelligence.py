from fastapi import APIRouter

from app.schemas.intelligence import AnalysisRequest, IntelligenceResponse
from app.services.cache.memory import request_cache
from app.services.disaster_engine.engine import DisasterEngine
from app.services.geospatial.search import resolve_search

router = APIRouter()
engine = DisasterEngine()


@router.post("/analyze", response_model=IntelligenceResponse)
def analyze_location(payload: AnalysisRequest) -> IntelligenceResponse:
    resolved = resolve_search(payload.query)
    cache_key = f"{round(resolved.coordinates.latitude, 4)}:{round(resolved.coordinates.longitude, 4)}"

    cached = request_cache.get(cache_key)
    if cached is not None:
        return cached

    response = engine.analyze(resolved)
    request_cache.set(cache_key, response)
    return response


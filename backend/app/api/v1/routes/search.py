from fastapi import APIRouter, Depends

from app.schemas.common import APIResponse
from app.schemas.intelligence import AnalysisResult
from app.schemas.search import SearchRequest
from app.services.search.service import SearchService, get_search_service

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=APIResponse[AnalysisResult])
async def search_endpoint(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service),
):
    """
    Search layer entrypoint. Accepts a city name or coordinates.
    """
    data = await search_service.search(request)
    return APIResponse(data=data)

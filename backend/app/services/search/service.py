from fastapi import Depends, HTTPException

from app.core.cache.keys import CacheCategory, CacheKeyBuilder
from app.core.cache.manager import cache_manager
from app.core.logging import get_logger
from app.schemas.geospatial import Coordinates
from app.schemas.intelligence import AnalysisResult
from app.schemas.search import SearchRequest
from app.services.analysis.service import AnalysisService, get_analysis_service
from app.services.geospatial import GeospatialService, get_geospatial_service

logger = get_logger(__name__)


class SearchService:
    def __init__(
        self,
        geospatial_service: GeospatialService,
        analysis_service: AnalysisService,
    ):
        self.geospatial_service = geospatial_service
        self.analysis_service = analysis_service

    async def search(self, request: SearchRequest) -> AnalysisResult:
        logger.info(
            "Starting search orchestration",
            extra={
                "query": request.query,
                "lat": request.latitude,
                "lon": request.longitude,
            },
        )

        if request.query:
            cache_key = CacheKeyBuilder.location_search(request.query)
        else:
            cache_key = CacheKeyBuilder.coordinates(
                CacheCategory.LOCATION_SEARCH,
                request.latitude,  # type: ignore
                request.longitude,  # type: ignore
            )

        async def fetch_analysis():
            location_name = ""
            coordinates = None

            if request.query:
                logger.info("Resolving city search query")
                results = await self.geospatial_service.search_location(request.query)
                if not results:
                    raise HTTPException(status_code=404, detail="Location not found")
                location_name = results[0].name
                coordinates = results[0].coordinates
            else:
                logger.info("Resolving coordinate search")
                coordinates = Coordinates(
                    lat=request.latitude, lon=request.longitude  # type: ignore
                )
                rev_result = await self.geospatial_service.reverse_geocode(coordinates)
                location_name = rev_result.name

            logger.info(
                "Executing disaster analysis", extra={"location_name": location_name}
            )
            analysis_result = await self.analysis_service.analyze(
                location_name, coordinates
            )
            return analysis_result

        # Deduplicated Cache Fetch
        try:
            analysis_result, hit = await cache_manager.get_or_fetch(
                cache_key, fetch_analysis
            )
            analysis_result.metadata["cache_hit"] = hit
            if hit:
                logger.info("Cache hit", extra={"cache_key": cache_key})
            else:
                logger.info("Cache miss", extra={"cache_key": cache_key})
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.warning(
                "Cache flow failed, proceeding to direct analysis",
                extra={"error": str(e), "cache_key": cache_key},
            )
            analysis_result = await fetch_analysis()
            analysis_result.metadata["cache_hit"] = False

        logger.info("Search orchestration complete")
        return analysis_result


def get_search_service(
    geospatial_service: GeospatialService = Depends(get_geospatial_service),
    analysis_service: AnalysisService = Depends(get_analysis_service),
) -> SearchService:
    return SearchService(geospatial_service, analysis_service)

from fastapi import Depends, HTTPException

from app.core.logging import get_logger
from app.schemas.geospatial import Coordinates
from app.schemas.intelligence import AnalysisResult
from app.schemas.search import SearchRequest
from app.services.analysis.service import AnalysisService, get_analysis_service
from app.services.cache.service import CacheKeyBuilder, CacheService, get_cache_service
from app.services.geospatial import GeospatialService, get_geospatial_service

logger = get_logger(__name__)


class SearchService:
    def __init__(
        self,
        geospatial_service: GeospatialService,
        analysis_service: AnalysisService,
        cache_service: CacheService,
    ):
        self.geospatial_service = geospatial_service
        self.analysis_service = analysis_service
        self.cache_service = cache_service

    async def search(self, request: SearchRequest) -> AnalysisResult:
        logger.info(
            "Starting search orchestration",
            extra={
                "query": request.query,
                "lat": request.latitude,
                "lon": request.longitude,
            },
        )

        # 1. Build cache key
        if request.query:
            cache_key = CacheKeyBuilder.location(request.query)
        else:
            cache_key = CacheKeyBuilder.coordinates(
                request.latitude, request.longitude  # type: ignore
            )

        # 2. Cache Lookup
        try:
            cached_result = self.cache_service.get(cache_key)
            if cached_result:
                logger.info("Cache hit", extra={"cache_key": cache_key})
                cached_result.metadata["cache_hit"] = True
                return cached_result
        except Exception as e:
            logger.warning(
                "Cache lookup failed, proceeding to analysis",
                extra={"error": str(e), "cache_key": cache_key},
            )

        logger.info("Cache miss", extra={"cache_key": cache_key})

        location_name = ""
        coordinates = None

        if request.query:
            logger.info("Resolving city search query")
            results = await self.geospatial_service.search_location(request.query)
            if not results:
                raise HTTPException(status_code=404, detail="Location not found")

            # Use the first result
            location_name = results[0].name
            coordinates = results[0].coordinates
        else:
            logger.info("Resolving coordinate search")
            # We know latitude and longitude are not None due to validation
            coordinates = Coordinates(lat=request.latitude, lon=request.longitude)  # type: ignore
            rev_result = await self.geospatial_service.reverse_geocode(coordinates)
            location_name = rev_result.name

        logger.info(
            "Executing disaster analysis", extra={"location_name": location_name}
        )
        analysis_result = await self.analysis_service.analyze(
            location_name, coordinates
        )

        analysis_result.metadata["cache_hit"] = False

        # 3. Cache Store
        try:
            self.cache_service.set(cache_key, analysis_result)
        except Exception as e:
            logger.warning(
                "Cache store failed",
                extra={"error": str(e), "cache_key": cache_key},
            )

        logger.info("Search orchestration complete")
        return analysis_result


def get_search_service(
    geospatial_service: GeospatialService = Depends(get_geospatial_service),
    analysis_service: AnalysisService = Depends(get_analysis_service),
    cache_service: CacheService = Depends(get_cache_service),
) -> SearchService:
    return SearchService(geospatial_service, analysis_service, cache_service)

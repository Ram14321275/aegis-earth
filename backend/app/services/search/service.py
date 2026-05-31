from fastapi import Depends, HTTPException

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

        logger.info("Search orchestration complete")
        return analysis_result


def get_search_service(
    geospatial_service: GeospatialService = Depends(get_geospatial_service),
    analysis_service: AnalysisService = Depends(get_analysis_service),
) -> SearchService:
    return SearchService(geospatial_service, analysis_service)

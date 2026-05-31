from fastapi import APIRouter, Depends

from app.schemas.common import APIResponse
from app.schemas.geospatial import LocationSearchResponse, ReverseGeocodeResponse, Coordinates
from app.services.geospatial import GeospatialService, get_geospatial_service
from app.validators.geospatial import validate_search_query, validate_coordinates

router = APIRouter(prefix="/geospatial", tags=["geospatial"])


@router.get("/search", response_model=APIResponse[list[LocationSearchResponse]])
async def search_location(
    query: str = Depends(validate_search_query),
    geospatial_service: GeospatialService = Depends(get_geospatial_service)
):
    """
    Search for a location by name.
    """
    data = await geospatial_service.search_location(query)
    return APIResponse(data=data)


@router.get("/reverse", response_model=APIResponse[ReverseGeocodeResponse])
async def reverse_geocode(
    coordinates: Coordinates = Depends(validate_coordinates),
    geospatial_service: GeospatialService = Depends(get_geospatial_service)
):
    """
    Reverse geocode coordinates into a location name.
    """
    data = await geospatial_service.reverse_geocode(coordinates)
    return APIResponse(data=data)

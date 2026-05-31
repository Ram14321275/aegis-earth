from app.schemas.geospatial import LocationSearchResponse, ReverseGeocodeResponse, Coordinates

class GeospatialService:
    async def search_location(self, query: str) -> list[LocationSearchResponse]:
        """
        Mock implementation of location search.
        In the future, this will integrate with an external geocoding API or database.
        """
        # Return mocked data
        return [
            LocationSearchResponse(
                name=f"Mocked Location for '{query}'",
                coordinates=Coordinates(lat=37.7749, lon=-122.4194),
                confidence=0.9,
                bounding_box=[-122.5, 37.7, -122.3, 37.8]
            )
        ]

    async def reverse_geocode(self, coordinates: Coordinates) -> ReverseGeocodeResponse:
        """
        Mock implementation of reverse geocoding.
        In the future, this will integrate with an external geocoding API.
        """
        return ReverseGeocodeResponse(
            name=f"Mocked Place at {coordinates.lat:.4f}, {coordinates.lon:.4f}",
            country="Mock Country",
            region="Mock Region"
        )

# Dependency injection helper
def get_geospatial_service() -> GeospatialService:
    return GeospatialService()

from app.db.models.location import Location
from app.db.repositories.base_repository import BaseRepository


class LocationRepository(BaseRepository[Location]):
    pass


location_repo = LocationRepository(Location)

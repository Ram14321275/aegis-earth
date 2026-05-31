from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.location_search import LocationSearch
from app.db.repositories.base import BaseRepository


class LocationRepository(BaseRepository[LocationSearch]):
    def __init__(self, session: AsyncSession):
        super().__init__(LocationSearch, session)

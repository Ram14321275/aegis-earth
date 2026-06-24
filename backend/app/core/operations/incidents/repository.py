from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.repositories.base_repository import BaseRepository
from app.db.models.operations import IncidentModel

class IncidentRepository(BaseRepository[IncidentModel]):
    def __init__(self):
        super().__init__(IncidentModel)
        
    async def get_by_status(self, session: AsyncSession, status: str, limit: int = 100) -> List[IncidentModel]:
        query = self._get_base_query().filter(self.model.status == status).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())

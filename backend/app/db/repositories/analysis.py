from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analysis_record import AnalysisRecord
from app.db.repositories.base import BaseRepository


class AnalysisRepository(BaseRepository[AnalysisRecord]):
    def __init__(self, session: AsyncSession):
        super().__init__(AnalysisRecord, session)

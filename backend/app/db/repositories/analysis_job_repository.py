from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.analysis_job import AnalysisJob
from app.db.repositories.base_repository import BaseRepository
from app.observability.metrics import metrics_store


class AnalysisJobRepository(BaseRepository[AnalysisJob]):
    def __init__(self):
        super().__init__(AnalysisJob)

    async def get_by_job_id(
        self, session: AsyncSession, job_id: str
    ) -> Optional[AnalysisJob]:
        try:
            result = await session.execute(
                select(AnalysisJob).filter(AnalysisJob.job_id == job_id)
            )
            obj = result.scalars().first()
            return obj
        except Exception as e:
            metrics_store.record_db_query(0, False)
            raise e


analysis_job_repository = AnalysisJobRepository()

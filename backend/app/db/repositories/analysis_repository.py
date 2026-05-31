from app.db.models.analysis import Analysis
from app.db.repositories.base_repository import BaseRepository


class AnalysisRepository(BaseRepository[Analysis]):
    pass


analysis_repo = AnalysisRepository(Analysis)

from app.db.models.risk import RiskAssessment
from app.db.repositories.base_repository import BaseRepository


class RiskRepository(BaseRepository[RiskAssessment]):
    pass


risk_repo = RiskRepository(RiskAssessment)

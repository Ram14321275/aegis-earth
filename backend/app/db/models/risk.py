from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import TenantAwareModel


class RiskAssessment(TenantAwareModel):
    __tablename__ = "risk_assessments"

    analysis_id: Mapped[str] = mapped_column(
        String, ForeignKey("analyses.id"), index=True
    )
    risk_score: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String, index=True)
    confidence: Mapped[float] = mapped_column(Float)

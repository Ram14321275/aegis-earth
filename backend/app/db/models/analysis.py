from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import TenantAwareModel


class Analysis(TenantAwareModel):
    __tablename__ = "analyses"

    location_id: Mapped[str] = mapped_column(
        String, ForeignKey("locations.id"), index=True
    )
    hazard_type: Mapped[str] = mapped_column(String)
    analysis_version: Mapped[str] = mapped_column(String)
    source: Mapped[str] = mapped_column(String)

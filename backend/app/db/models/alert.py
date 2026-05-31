from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModel


class Alert(BaseModel):
    __tablename__ = "alerts"

    analysis_id: Mapped[str] = mapped_column(
        String, ForeignKey("analyses.id"), index=True
    )
    severity: Mapped[str] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(String)

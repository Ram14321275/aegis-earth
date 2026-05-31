from sqlalchemy import Float, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModel


class LocationSearch(BaseModel):
    __tablename__ = "location_searches"

    query: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    city: Mapped[str | None] = mapped_column(String, nullable=True)
    state_province: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (Index("ix_location_searches_created_at", "created_at"),)

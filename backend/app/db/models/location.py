from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModel


class Location(BaseModel):
    __tablename__ = "locations"

    city: Mapped[str] = mapped_column(String, index=True)
    state_province: Mapped[str | None] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    query: Mapped[str] = mapped_column(String)

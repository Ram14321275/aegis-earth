from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geography

from app.db.base import BaseModel


class Location(BaseModel):
    __tablename__ = "locations"

    city: Mapped[str] = mapped_column(String, index=True)
    state_province: Mapped[str | None] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    query: Mapped[str] = mapped_column(String)
    
    # Geography type automatically creates a GiST index by default when spatial_index=True
    point_geometry: Mapped[str | None] = mapped_column(
        Geography(geometry_type='POINT', srid=4326, spatial_index=True),
        nullable=True
    )

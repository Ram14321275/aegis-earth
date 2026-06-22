from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModel


class Tenant(BaseModel):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String, index=True)
    tier: Mapped[str] = mapped_column(String, default="standard")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

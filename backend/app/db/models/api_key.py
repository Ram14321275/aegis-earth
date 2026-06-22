from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import TenantAwareModel


class APIKey(TenantAwareModel):
    __tablename__ = "api_keys"

    key_hash: Mapped[str] = mapped_column(String, unique=True, index=True)
    prefix: Mapped[str] = mapped_column(String, index=True)
    name: Mapped[str] = mapped_column(String)
    user_id: Mapped[str | None] = mapped_column(String, ForeignKey("users.id"), nullable=True)
    scopes: Mapped[list[str]] = mapped_column(JSON, default=list)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)

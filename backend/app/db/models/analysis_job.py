from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Float, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModel


class AnalysisJob(BaseModel):
    __tablename__ = "analysis_jobs"

    job_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    location_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("locations.id"), index=True, nullable=True
    )
    analysis_type: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(String, index=True)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    worker_id: Mapped[str | None] = mapped_column(String, nullable=True)
    
    queued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    heartbeat_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0)
    execution_time_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    metadata_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

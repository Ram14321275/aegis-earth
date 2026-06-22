from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import TenantAwareModel, Base

class JobAttempt(TenantAwareModel):
    __tablename__ = "job_attempts"

    job_id: Mapped[str] = mapped_column(String, ForeignKey("analysis_jobs.job_id", ondelete="CASCADE"), index=True)
    attempt_number: Mapped[int] = mapped_column(Integer)
    worker_id: Mapped[str | None] = mapped_column(String, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String) # SUCCESS, FAILED, CANCELLED
    logs: Mapped[dict | None] = mapped_column(JSON, nullable=True)

class JobFailure(TenantAwareModel):
    __tablename__ = "job_failures"

    job_id: Mapped[str] = mapped_column(String, ForeignKey("analysis_jobs.job_id", ondelete="CASCADE"), index=True)
    attempt_number: Mapped[int] = mapped_column(Integer)
    failure_reason: Mapped[str] = mapped_column(String)
    stack_trace: Mapped[str | None] = mapped_column(String, nullable=True)

class IdempotencyRecord(TenantAwareModel):
    __tablename__ = "idempotency_records"

    idempotency_key: Mapped[str] = mapped_column(String, unique=True, index=True)
    job_id: Mapped[str] = mapped_column(String, index=True)
    response_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class DeduplicationLock(TenantAwareModel):
    __tablename__ = "deduplication_locks"

    fingerprint: Mapped[str] = mapped_column(String, unique=True, index=True)
    job_id: Mapped[str] = mapped_column(String, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

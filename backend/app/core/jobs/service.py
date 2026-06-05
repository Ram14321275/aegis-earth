import uuid
import time
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ValidationError
from app.core.jobs.manager import job_queue_manager
from app.core.jobs.models import JobCreate, JobUpdate, JobResponse
from app.core.jobs.statuses import JobStatus
from app.core.jobs.validators import validate_analysis_type, validate_job_transition
from app.db.models.analysis_job import AnalysisJob
from app.db.repositories.analysis_job_repository import analysis_job_repository
from app.observability.metrics import metrics_store


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class JobService:
    async def create_job(self, session: AsyncSession, create_data: JobCreate) -> JobResponse:
        validate_analysis_type(create_data.analysis_type)
        
        job_id = f"job-{uuid.uuid4()}"
        
        job_obj = {
            "job_id": job_id,
            "status": JobStatus.PENDING.value,
            "analysis_type": create_data.analysis_type,
            "location_id": create_data.location_id,
            "priority": create_data.priority,
            "max_retries": create_data.max_retries,
            "metadata_data": create_data.metadata_data,
        }
        
        db_job = await analysis_job_repository.create(session, obj_in=job_obj)
        metrics_store.record_job_created()
        
        # Enqueue the job immediately
        await self.update_status(session, job_id, JobStatus.QUEUED)
        await job_queue_manager.enqueue(job_id, priority=create_data.priority)
        
        return self._to_response(db_job)

    async def get_job(self, session: AsyncSession, job_id: str) -> JobResponse:
        db_job = await analysis_job_repository.get_by_job_id(session, job_id)
        if not db_job:
            raise NotFoundError(f"Job {job_id} not found")
        return self._to_response(db_job)

    async def update_status(
        self, 
        session: AsyncSession, 
        job_id: str, 
        new_status: JobStatus, 
        worker_id: Optional[str] = None,
        error_message: Optional[str] = None,
        execution_time_ms: Optional[float] = None
    ) -> JobResponse:
        db_job = await analysis_job_repository.get_by_job_id(session, job_id)
        if not db_job:
            raise NotFoundError(f"Job {job_id} not found")
            
        validate_job_transition(db_job.status, new_status)
        
        db_job.status = new_status.value
        
        now = get_utc_now()
        
        if new_status == JobStatus.QUEUED:
            db_job.queued_at = now
        elif new_status == JobStatus.RUNNING:
            if db_job.started_at is None:
                db_job.started_at = now
            db_job.worker_id = worker_id
        elif new_status == JobStatus.COMPLETED:
            db_job.completed_at = now
            db_job.progress_percent = 100.0
            if execution_time_ms:
                db_job.execution_time_ms = execution_time_ms
            metrics_store.record_job_completed()
        elif new_status == JobStatus.FAILED:
            db_job.completed_at = now
            if error_message:
                db_job.error_message = error_message
            if execution_time_ms:
                db_job.execution_time_ms = execution_time_ms
            metrics_store.record_job_failed()
        elif new_status == JobStatus.RETRYING:
            db_job.retry_count += 1
            if error_message:
                db_job.error_message = error_message
            metrics_store.record_job_retried()

        await session.commit()
        await session.refresh(db_job)
        
        return self._to_response(db_job)

    async def cancel_job(self, session: AsyncSession, job_id: str) -> JobResponse:
        return await self.update_status(session, job_id, JobStatus.CANCELLED)

    def _to_response(self, db_job: AnalysisJob) -> JobResponse:
        return JobResponse(
            job_id=db_job.job_id,
            analysis_type=db_job.analysis_type,
            status=JobStatus(db_job.status),
            progress_percent=db_job.progress_percent,
            created_at=db_job.created_at,
            queued_at=db_job.queued_at,
            started_at=db_job.started_at,
            completed_at=db_job.completed_at,
            error_message=db_job.error_message,
            retry_count=db_job.retry_count,
            metadata_data=db_job.metadata_data
        )

job_service = JobService()

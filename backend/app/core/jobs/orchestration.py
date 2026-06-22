import logging
import uuid
from typing import Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.jobs.models import JobCreate, JobResponse
from app.core.jobs.statuses import JobStatus
from app.core.jobs.idempotency import idempotency_manager
from app.core.jobs.deduplication import deduplication_manager
from app.core.jobs.scheduler import job_scheduler
from app.db.repositories.analysis_job_repository import analysis_job_repository
from app.observability.metrics import metrics_store
from app.core.security.tenants import get_current_tenant_id

logger = logging.getLogger(__name__)

class JobOrchestrator:
    async def handle_analysis_request(
        self, 
        session: AsyncSession, 
        create_data: JobCreate,
        idempotency_key: Optional[str] = None
    ) -> JobResponse:
        
        tenant_id = get_current_tenant_id()
        
        # 1. Idempotency Check
        if idempotency_key:
            record = await idempotency_manager.get_idempotency_record(session, idempotency_key)
            if record:
                logger.info(f"Idempotency hit for {idempotency_key}, returning existing job {record.job_id}")
                # Ideally emit metric idempotency_reuse_total
                metrics_store.record_idempotency_reuse()
                db_job = await analysis_job_repository.get_by_job_id(session, record.job_id)
                if db_job:
                    return self._to_response(db_job)

        # 2. Preparation
        job_id = f"job-{uuid.uuid4()}"
        correlation_id = f"corr-{uuid.uuid4()}"
        
        payload = create_data.model_dump()
        payload["job_id"] = job_id
        payload["correlation_id"] = correlation_id
        payload["tenant_id"] = tenant_id

        # 3. Deduplication Check
        acquired, existing_job_id = await deduplication_manager.acquire_dedup_lock(payload)
        if not acquired and existing_job_id:
            logger.info(f"Deduplication hit. Request matches active job {existing_job_id}")
            metrics_store.record_deduplication_save()
            db_job = await analysis_job_repository.get_by_job_id(session, existing_job_id)
            if db_job:
                # Still create idempotency record mapping to existing job if requested
                if idempotency_key:
                    await idempotency_manager.create_idempotency_record(session, idempotency_key, existing_job_id)
                return self._to_response(db_job)

        # 4. Persistence (PENDING state)
        job_obj = {
            "job_id": job_id,
            "correlation_id": correlation_id,
            "status": JobStatus.PENDING.value,
            "analysis_type": create_data.analysis_type,
            "hazard_type": create_data.analysis_type,
            "location_id": create_data.location_id,
            "priority": create_data.priority,
            "max_retries": create_data.max_retries,
            "metadata_data": create_data.metadata_data,
        }
        db_job = await analysis_job_repository.create(session, obj_in=job_obj)
        metrics_store.record_job_created()
        
        if idempotency_key:
            await idempotency_manager.create_idempotency_record(session, idempotency_key, job_id)

        # 5. Scheduling & Enqueuing
        await self.update_job_status(session, job_id, JobStatus.QUEUED)
        await job_scheduler.schedule(payload)

        return self._to_response(db_job)

    async def update_job_status(self, session: AsyncSession, job_id: str, new_status: JobStatus) -> None:
        db_job = await analysis_job_repository.get_by_job_id(session, job_id)
        if db_job:
            db_job.status = new_status.value
            await session.commit()
            
            # Domain Event Broadcast (Simulated streaming hook)
            # stream_publisher.publish("job.status.changed", db_job)

    def _to_response(self, db_job: Any) -> JobResponse:
        return JobResponse(
            job_id=db_job.job_id,
            analysis_type=db_job.analysis_type,
            status=JobStatus(db_job.status),
            progress_percent=db_job.progress_percent,
            created_at=db_job.created_at,
            queued_at=db_job.queued_at,
            started_at=db_job.started_at,
            completed_at=db_job.completed_at,
            error_message=db_job.failure_reason,
            retry_count=db_job.retry_count,
            metadata_data=db_job.metadata_data
        )

job_orchestrator = JobOrchestrator()

import asyncio
import time
from typing import Optional

from app.core.jobs.manager import job_queue_manager
from app.core.jobs.service import job_service
from app.core.jobs.statuses import JobStatus
from app.core.workers.manager import worker_manager
from app.core.workers.models import WorkerStatus
from app.core.workers.heartbeat import HeartbeatSystem
from app.db.session import AsyncSessionLocal
from app.observability.metrics import metrics_store
from app.core.processing.pipeline import sentinel_processing_pipeline
from app.core.satellite.service import satellite_service


class WorkerExecutor:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.running = False
        self._task: Optional[asyncio.Task] = None
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._heartbeat_system = HeartbeatSystem(interval_seconds=15)

    async def start(self):
        if self.running:
            return
            
        self.running = True
        worker_manager.register_worker(self.worker_id)
        
        self._heartbeat_task = asyncio.create_task(
            self._heartbeat_system.run(self.worker_id, worker_manager.update_heartbeat)
        )
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        self.running = False
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        worker_manager.unregister_worker(self.worker_id)

    async def _run_loop(self):
        try:
            while self.running:
                # Wait for a job from the queue
                worker_manager.set_worker_status(self.worker_id, WorkerStatus.IDLE)
                
                # We use a short sleep to prevent blocking entirely if the queue is empty
                # In a real system (Redis/Celery) we'd use BLPOP or equivalent.
                job_id = await job_queue_manager.dequeue()
                
                if not job_id:
                    await asyncio.sleep(1)
                    continue

                await self._process_job(job_id)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            worker_manager.set_worker_status(self.worker_id, WorkerStatus.FAILED)
            raise e

    async def _process_job(self, job_id: str):
        worker_manager.set_worker_status(self.worker_id, WorkerStatus.BUSY, active_job=job_id)
        start_time = time.time()
        
        try:
            async with AsyncSessionLocal() as session:
                # Mark as RUNNING
                job = await job_service.update_status(
                    session, job_id, JobStatus.RUNNING, worker_id=self.worker_id
                )
                
                # Mock heavy processing
                job_db = await job_service.get_job(session, job_id)
                
                if job_db.analysis_type == "PROCESS_SENTINEL":
                    provider_id = job_db.metadata_data.get("provider_id")
                    scene_id = job_db.metadata_data.get("scene_id")
                    
                    if not provider_id or not scene_id:
                        raise ValueError("Missing provider_id or scene_id in metadata_data")
                        
                    # Fetch Scene
                    scene = await satellite_service.fetch_scene(provider_id, scene_id)
                    
                    # Process Scene
                    result = await sentinel_processing_pipeline.process_scene(scene)
                    
                    if not result.success:
                        raise RuntimeError(f"Processing failed: {result.error_message}")
                else:
                    await asyncio.sleep(2.0)
                
                execution_time_ms = (time.time() - start_time) * 1000
                metrics_store.record_worker_execution(execution_time_ms)
                
                # Complete the job
                await job_service.update_status(
                    session, job_id, JobStatus.COMPLETED, execution_time_ms=execution_time_ms
                )
                worker_manager.record_job_processed(self.worker_id)
                
        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            metrics_store.record_worker_execution(execution_time_ms)
            
            # Handle failure/retry
            async with AsyncSessionLocal() as session:
                job = await job_service.get_job(session, job_id)
                if job.retry_count < job.max_retries:
                    await job_service.update_status(
                        session, job_id, JobStatus.RETRYING, error_message=str(e)
                    )
                    # Re-enqueue immediately or with backoff (immediate for MVP)
                    await job_queue_manager.enqueue(job_id)
                else:
                    await job_service.update_status(
                        session, job_id, JobStatus.FAILED, error_message=str(e), execution_time_ms=execution_time_ms
                    )

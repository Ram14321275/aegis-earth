import asyncio
import pytest

from app.core.workers.manager import worker_manager
from app.core.workers.executor import WorkerExecutor
from app.core.workers.models import WorkerStatus
from app.core.jobs.manager import job_queue_manager
from app.core.jobs.service import job_service
from app.core.jobs.statuses import JobStatus

class MockQueue:
    def __init__(self):
        self.q = []
    async def enqueue(self, qname, payload, priority=0):
        self.q.append(payload)
    async def dequeue(self, qname, timeout=0):
        if self.q: return self.q.pop(0)
        return None
    async def get_depth(self, qname):
        return len(self.q)

job_queue_manager._queue = MockQueue()

@pytest.mark.anyio
async def test_worker_registration():
    executor = WorkerExecutor("test-worker-1")
    await executor.start()
    
    assert "test-worker-1" in worker_manager.workers
    assert worker_manager.workers["test-worker-1"].status == WorkerStatus.IDLE
    
    await executor.stop()
    assert "test-worker-1" not in worker_manager.workers

from unittest.mock import AsyncMock, patch

@pytest.mark.anyio
@patch("app.core.jobs.service.analysis_job_repository.create", new_callable=AsyncMock)
@patch("app.core.jobs.service.analysis_job_repository.get_by_job_id", new_callable=AsyncMock)
async def test_job_execution(mock_get, mock_create):
    from app.db.models.analysis_job import AnalysisJob
    import uuid
    from datetime import datetime, timezone
    
    dummy_job = AnalysisJob(
        job_id=f"job-{uuid.uuid4()}",
        status=JobStatus.PENDING.value,
        analysis_type="flood",
        location_id="loc-1",
        priority=1,
        max_retries=3,
        created_at=datetime.now(timezone.utc),
        progress_percent=0.0,
        retry_count=0
    )
    mock_create.return_value = dummy_job
    mock_get.return_value = dummy_job
    
    executor = WorkerExecutor("test-worker-2")
    await executor.start()
    
    # Mock job creation
    from app.core.jobs.models import JobCreate
    job_create = JobCreate(analysis_type="flood", location_id="loc-1")
    
    # We mock AsyncSessionLocal directly in the executor inside service updates
    mock_session = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    with patch("app.db.session.AsyncSessionLocal", return_value=mock_session):
        with patch("app.core.workers.executor.AsyncSessionLocal", return_value=mock_session):
            job_response = await job_service.create_job(mock_session, job_create)
            
            # Wait for worker to pick it up (sleep briefly)
            await asyncio.sleep(0.5)
            
            # Check status
            updated_job = await job_service.get_job(mock_session, job_response.job_id)
            assert updated_job.status in (JobStatus.RUNNING.value, JobStatus.COMPLETED.value)
    
    await executor.stop()

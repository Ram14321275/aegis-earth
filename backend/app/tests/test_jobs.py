import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.core.jobs.statuses import JobStatus
from app.db.session import get_db_session

mock_session = AsyncMock()
app.dependency_overrides[get_db_session] = lambda: mock_session

client = TestClient(app)

@patch("app.core.jobs.service.analysis_job_repository.create", new_callable=AsyncMock)
@patch("app.core.jobs.service.analysis_job_repository.get_by_job_id", new_callable=AsyncMock)
def test_job_creation(mock_get, mock_create):
    from app.db.models.analysis_job import AnalysisJob
    import uuid
    from datetime import datetime, timezone
    
    dummy_job = AnalysisJob(
        job_id=f"job-{uuid.uuid4()}",
        status=JobStatus.PENDING.value,
        analysis_type="flood",
        location_id="loc-123",
        priority=1,
        max_retries=3,
        created_at=datetime.now(timezone.utc),
        progress_percent=0.0,
        retry_count=0
    )
    mock_create.return_value = dummy_job
    mock_get.return_value = dummy_job
    mock_session.refresh = AsyncMock()
    
    response = client.post("/api/v1/jobs", json={
        "analysis_type": "flood",
        "location_id": "loc-123",
        "priority": 1,
        "max_retries": 3,
        "metadata_data": {"source": "test"}
    })
    
    assert response.status_code == 201
    data = response.json()
    assert "job_id" in data
    assert data["status"] in (JobStatus.QUEUED.value, JobStatus.PENDING.value)
    
def test_invalid_analysis_type():
    response = client.post("/api/v1/jobs", json={
        "analysis_type": "invalid_type"
    })
    
    assert response.status_code == 422

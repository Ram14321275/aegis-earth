from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field

from app.core.jobs.statuses import JobStatus

class JobCreate(BaseModel):
    analysis_type: str
    location_id: Optional[str] = None
    priority: int = 0
    max_retries: int = 3
    metadata_data: Dict[str, Any] = Field(default_factory=dict)

class JobUpdate(BaseModel):
    status: Optional[JobStatus] = None
    progress_percent: Optional[float] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[float] = None

from pydantic import BaseModel, Field, ConfigDict

class JobResponse(BaseModel):
    job_id: str
    analysis_type: str
    status: JobStatus
    progress_percent: float
    created_at: datetime
    queued_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    metadata_data: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)

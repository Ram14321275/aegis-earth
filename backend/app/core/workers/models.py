from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

class WorkerStatus(str, Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"
    FAILED = "FAILED"

class WorkerState(BaseModel):
    worker_id: str
    status: WorkerStatus
    active_job: Optional[str] = None
    started_at: datetime
    last_heartbeat: datetime
    jobs_processed: int = 0

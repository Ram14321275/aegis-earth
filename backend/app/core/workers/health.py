from typing import Dict

from app.core.workers.manager import worker_manager
from app.core.workers.models import WorkerStatus

def get_worker_system_health() -> Dict[str, int]:
    active = 0
    idle = 0
    busy = 0
    
    for worker in worker_manager.workers.values():
        if worker.status in (WorkerStatus.IDLE, WorkerStatus.BUSY):
            active += 1
        if worker.status == WorkerStatus.IDLE:
            idle += 1
        if worker.status == WorkerStatus.BUSY:
            busy += 1
            
    return {
        "active": active,
        "idle": idle,
        "busy": busy
    }

import asyncio
from typing import Dict
from datetime import datetime, timezone

from app.core.workers.models import WorkerState, WorkerStatus
from app.observability.metrics import metrics_store

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class WorkerManager:
    def __init__(self):
        self.workers: Dict[str, WorkerState] = {}
        
    def register_worker(self, worker_id: str) -> None:
        self.workers[worker_id] = WorkerState(
            worker_id=worker_id,
            status=WorkerStatus.IDLE,
            started_at=get_utc_now(),
            last_heartbeat=get_utc_now()
        )
        self._update_metrics()
        
    def unregister_worker(self, worker_id: str) -> None:
        if worker_id in self.workers:
            self.workers[worker_id].status = WorkerStatus.OFFLINE
            # In a real distributed system we might remove them after a while
            del self.workers[worker_id]
        self._update_metrics()
        
    def update_heartbeat(self, worker_id: str, timestamp: datetime) -> None:
        if worker_id in self.workers:
            self.workers[worker_id].last_heartbeat = timestamp
            
    def set_worker_status(self, worker_id: str, status: WorkerStatus, active_job: str | None = None) -> None:
        if worker_id in self.workers:
            self.workers[worker_id].status = status
            self.workers[worker_id].active_job = active_job
            if status == WorkerStatus.FAILED:
                metrics_store.record_worker_failure()
            self._update_metrics()
            
    def record_job_processed(self, worker_id: str) -> None:
        if worker_id in self.workers:
            self.workers[worker_id].jobs_processed += 1
            
    def _update_metrics(self) -> None:
        active = sum(1 for w in self.workers.values() if w.status in (WorkerStatus.IDLE, WorkerStatus.BUSY))
        metrics_store.set_workers_active(active)

worker_manager = WorkerManager()

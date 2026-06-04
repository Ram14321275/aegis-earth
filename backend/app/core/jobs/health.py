from typing import Dict

from app.core.jobs.manager import job_queue_manager
from app.observability.metrics import metrics_store

async def get_job_system_health() -> Dict[str, int]:
    metrics = metrics_store.get_metrics()
    queue_depth = await job_queue_manager.get_depth()
    
    return {
        "queue_depth": queue_depth,
        "running": metrics.workers.workers_active_total, # Assuming active workers = running jobs for now
        "failed": metrics.jobs.jobs_failed_total
    }

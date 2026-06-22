from app.core.jobs.queue import redis_queue
from app.observability.metrics import metrics_store

class JobQueueManager:
    def __init__(self):
        self._queue = redis_queue
        self.queue_name = "default"

    async def enqueue(self, job_id: str, priority: int = 0) -> None:
        await self._queue.enqueue(self.queue_name, {"job_id": job_id}, priority=float(priority))
        depth = await self._queue.get_depth(self.queue_name)
        metrics_store.update_queue_depth(depth)

    async def dequeue(self) -> str | None:
        payload = await self._queue.dequeue(self.queue_name)
        if payload and "job_id" in payload:
            depth = await self._queue.get_depth(self.queue_name)
            metrics_store.update_queue_depth(depth)
            return payload["job_id"]
        return None

    async def get_depth(self) -> int:
        return await self._queue.get_depth(self.queue_name)

job_queue_manager = JobQueueManager()

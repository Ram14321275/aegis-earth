from app.core.jobs.queue import InMemoryJobQueue
from app.observability.metrics import metrics_store

class JobQueueManager:
    def __init__(self):
        # Default to InMemoryJobQueue for MVP
        self._queue = InMemoryJobQueue()

    async def enqueue(self, job_id: str, priority: int = 0) -> None:
        await self._queue.enqueue(job_id, priority)
        depth = await self._queue.get_depth()
        metrics_store.update_queue_depth(depth)

    async def dequeue(self) -> str | None:
        job_id = await self._queue.dequeue()
        if job_id:
            depth = await self._queue.get_depth()
            metrics_store.update_queue_depth(depth)
        return job_id

    async def get_depth(self) -> int:
        return await self._queue.get_depth()

job_queue_manager = JobQueueManager()

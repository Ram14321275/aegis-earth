import asyncio
from typing import Optional

class JobQueue:
    async def enqueue(self, job_id: str, priority: int = 0) -> None:
        raise NotImplementedError
        
    async def dequeue(self) -> Optional[str]:
        raise NotImplementedError
        
    async def get_depth(self) -> int:
        raise NotImplementedError

class InMemoryJobQueue(JobQueue):
    def __init__(self):
        # We can use PriorityQueue if priority matters, but simple Queue is fine for MVP
        self._queue = asyncio.Queue()
        
    async def enqueue(self, job_id: str, priority: int = 0) -> None:
        await self._queue.put(job_id)
        
    async def dequeue(self) -> Optional[str]:
        return await self._queue.get()
        
    async def get_depth(self) -> int:
        return self._queue.qsize()

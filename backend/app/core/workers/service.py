import uuid
from typing import List

from app.core.workers.executor import WorkerExecutor

class WorkerService:
    def __init__(self):
        self.executors: List[WorkerExecutor] = []
        
    async def start_workers(self, count: int = 4):
        for _ in range(count):
            worker_id = f"worker-{uuid.uuid4().hex[:8]}"
            executor = WorkerExecutor(worker_id)
            self.executors.append(executor)
            await executor.start()
            
    async def stop_workers(self):
        for executor in self.executors:
            await executor.stop()
        self.executors.clear()

worker_service = WorkerService()

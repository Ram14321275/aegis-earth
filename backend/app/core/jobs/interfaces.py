from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime

class QueueInterface(ABC):
    @abstractmethod
    async def enqueue(self, queue_name: str, payload: Dict[str, Any], priority: float = 0.0) -> str:
        """Adds a job to the queue, returning a message ID or similar."""
        pass

    @abstractmethod
    async def dequeue(self, queue_name: str, timeout: int = 0) -> Optional[Dict[str, Any]]:
        """Removes and returns a job from the queue."""
        pass

    @abstractmethod
    async def ack(self, queue_name: str, message_id: str) -> None:
        """Acknowledges successful processing of a job."""
        pass

    @abstractmethod
    async def nack(self, queue_name: str, message_id: str) -> None:
        """Negative acknowledgment, potentially returning the job to the queue."""
        pass

class SchedulerInterface(ABC):
    @abstractmethod
    async def schedule(self, payload: Dict[str, Any], scheduled_at: Optional[datetime] = None) -> None:
        """Schedules a job for immediate or delayed execution based on advanced priority scoring."""
        pass

class WorkerInterface(ABC):
    @abstractmethod
    async def start(self) -> None:
        """Starts the worker, binding it to the queue and entering the processing loop."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Gracefully stops the worker, finishing current tasks and releasing leases."""
        pass

    @abstractmethod
    async def process_job(self, job_payload: Dict[str, Any]) -> None:
        """Processes a single job payload."""
        pass

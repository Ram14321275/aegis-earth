import json
import logging
from typing import Any, Dict, Optional

from app.core.cache.redis_client import redis_client
from app.core.jobs.interfaces import QueueInterface
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class RedisJobQueue(QueueInterface):
    """
    Redis implementation of QueueInterface utilizing Redis Lists (BLPOP/RPUSH).
    No redis logic should leak outside of this class.
    """
    def __init__(self, namespace: str = "aegis:queue"):
        self.namespace = namespace

    def _get_queue_key(self, queue_name: str) -> str:
        return f"{self.namespace}:{queue_name}"

    async def enqueue(self, queue_name: str, payload: Dict[str, Any], priority: float = 0.0) -> str:
        client = await redis_client.get_client()
        if not client:
            raise RuntimeError("Redis client unavailable for enqueue")
        
        queue_key = self._get_queue_key(queue_name)
        # We push to the left or right depending on priority.
        # For a full priority queue, we'd use ZADD. Here we simulate basic high/low by L/R push
        # or we just rely on the Scheduler to pick the right queue_name (e.g., 'high', 'default').
        # Using RPUSH for standard FIFO
        val = json.dumps(payload)
        await client.rpush(queue_key, val)
        return payload.get("job_id", "")

    async def dequeue(self, queue_name: str, timeout: int = 0) -> Optional[Dict[str, Any]]:
        client = await redis_client.get_client()
        if not client:
            return None
        
        queue_key = self._get_queue_key(queue_name)
        try:
            # BLPOP blocks until an item is available or timeout
            result = await client.blpop(queue_key, timeout=timeout)
            if result:
                _, val = result
                payload = json.loads(val)
                return payload
            return None
        except Exception as e:
            logger.error(f"Error dequeueing from {queue_key}: {e}")
            return None

    async def ack(self, queue_name: str, message_id: str) -> None:
        # With pure Redis Lists, popping removes it. 
        # A reliable queue would use RPOPLPUSH to a processing list.
        # For this checkpoint MVP, we assume popping is consuming.
        pass

    async def nack(self, queue_name: str, message_id: str) -> None:
        # In a real system, we'd move it back from the processing list to the queue.
        pass

    async def get_depth(self, queue_name: str) -> int:
        client = await redis_client.get_client()
        if not client:
            return 0
        return await client.llen(self._get_queue_key(queue_name))

redis_queue = RedisJobQueue()

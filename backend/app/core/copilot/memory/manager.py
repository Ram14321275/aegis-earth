import json
import logging
from typing import List
from datetime import timedelta

from app.core.copilot.models import MissionMemoryRecord
from app.core.cache.redis_client import redis_client
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class MissionMemoryManager:
    """
    Manages operational mission memory via Redis with 7-day TTL.
    Ensures memory remains tenant-isolated.
    """
    
    TTL_SECONDS = int(timedelta(days=7).total_seconds())

    def _build_key(self, tenant_id: str, mission_id: str, thread_id: str) -> str:
        return f"tenant:{tenant_id}:mission:{mission_id}:thread:{thread_id}"

    async def save_record(self, record: MissionMemoryRecord) -> None:
        client = await redis_client.get_client()
        if not client:
            logger.warning("Redis client unavailable. Cannot save memory record.")
            return

        key = self._build_key(record.tenant_id, record.mission_id, record.thread_id)
        
        try:
            data = record.model_dump_json()
            await client.rpush(key, data)
            await client.expire(key, self.TTL_SECONDS)
        except Exception as e:
            logger.error(f"Failed to save mission memory: {e}")

    async def get_thread(self, tenant_id: str, mission_id: str, thread_id: str) -> List[MissionMemoryRecord]:
        client = await redis_client.get_client()
        if not client:
            logger.warning("Redis client unavailable. Cannot fetch memory thread.")
            return []

        key = self._build_key(tenant_id, mission_id, thread_id)
        try:
            records_json = await client.lrange(key, 0, -1)
            if not records_json:
                return []
                
            records = []
            for r_json in records_json:
                records.append(MissionMemoryRecord.model_validate_json(r_json))
                
            return records
        except Exception as e:
            logger.error(f"Failed to fetch mission memory: {e}")
            metrics_store.record_command_center_action("mission_memory_evictions")
            return []

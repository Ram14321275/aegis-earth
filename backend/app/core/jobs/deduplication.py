import hashlib
import json
import logging
from typing import Any, Dict, Optional

from app.core.cache.redis_client import redis_client
from app.core.security.tenants import get_current_tenant_id

logger = logging.getLogger(__name__)

class DeduplicationManager:
    def _generate_fingerprint(
        self, 
        coordinates: str, 
        timeframe: str, 
        hazard_type: str, 
        analysis_version: str,
        provider_version: str,
        pipeline_version: str
    ) -> str:
        raw = f"{coordinates}|{timeframe}|{hazard_type}|{analysis_version}|{provider_version}|{pipeline_version}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    async def acquire_dedup_lock(self, payload: Dict[str, Any], ttl_seconds: int = 3600) -> tuple[bool, Optional[str]]:
        """
        Attempts to acquire a SET NX EX lock for deduplication.
        Returns (acquired_boolean, existing_job_id_if_not_acquired).
        """
        client = await redis_client.get_client()
        if not client:
            # Fallback to no deduplication if redis is unavailable
            return True, None

        metadata = payload.get("metadata_data", {}) or {}
        coordinates = str(payload.get("location_id", "global"))
        timeframe = metadata.get("timeframe", "now")
        hazard_type = payload.get("analysis_type", "unknown")
        analysis_version = metadata.get("analysis_version", "1.0")
        provider_version = metadata.get("provider_version", "1.0")
        pipeline_version = metadata.get("pipeline_version", "1.0")

        fingerprint = self._generate_fingerprint(
            coordinates, timeframe, hazard_type, analysis_version, provider_version, pipeline_version
        )
        
        tenant_id = get_current_tenant_id() or "system"
        lock_key = f"tenant:{tenant_id}:dedup:{fingerprint}"

        job_id = payload.get("job_id")

        # Atomic SET NX EX
        acquired = await client.set(lock_key, job_id, nx=True, ex=ttl_seconds)
        
        if acquired:
            return True, None
        else:
            # Lock exists, return the existing job_id
            existing_job_id = await client.get(lock_key)
            if existing_job_id:
                # Decoding since redis returns bytes
                if isinstance(existing_job_id, bytes):
                    return False, existing_job_id.decode("utf-8")
                return False, existing_job_id
            return True, None

    async def release_dedup_lock(self, fingerprint: str) -> None:
        client = await redis_client.get_client()
        if not client:
            return
        
        tenant_id = get_current_tenant_id() or "system"
        lock_key = f"tenant:{tenant_id}:dedup:{fingerprint}"
        await client.delete(lock_key)

deduplication_manager = DeduplicationManager()

import json
import logging
import uuid
from typing import Optional

from fastapi import HTTPException
from app.core.command_center.snapshots.engine import snapshot_engine
# Placeholder for our background job queue
from app.core.cache.redis import get_redis

logger = logging.getLogger(__name__)

class CommandCenterExportService:
    """
    Generates JSON, CSV, GeoJSON exports asynchronously.
    Operates strictly on immutable snapshots.
    """

    async def request_export(self, tenant_id: str, snapshot_id: str, format_type: str) -> str:
        """
        Validates the snapshot and enqueues an export job.
        """
        if format_type not in ["json", "csv", "geojson", "pdf"]:
            raise HTTPException(status_code=400, detail="Unsupported export format.")

        snapshot = await snapshot_engine.get_snapshot(snapshot_id)
        if not snapshot:
            raise HTTPException(status_code=404, detail="Snapshot not found.")

        if snapshot.tenant_id != tenant_id:
            raise HTTPException(status_code=403, detail="Access denied.")

        job_id = str(uuid.uuid4())
        
        # Enqueue job to background worker.
        # In MVP, we push a message to a Redis queue that a worker process listens to.
        try:
            redis = await get_redis()
            payload = {
                "job_id": job_id,
                "tenant_id": tenant_id,
                "snapshot_id": snapshot_id,
                "format": format_type,
                "status": "pending"
            }
            # Add to a mocked jobs list and hash
            await redis.hset(f"job:{job_id}", mapping=payload)
            await redis.lpush("export_queue", json.dumps(payload))
            logger.info(f"Queued export job {job_id} for snapshot {snapshot_id}")
        except Exception as e:
            logger.error(f"Failed to queue export job: {e}")
            raise HTTPException(status_code=500, detail="Internal export queuing error.")

        return job_id

    async def get_export_status(self, tenant_id: str, job_id: str) -> Optional[dict]:
        """
        Retrieves the status of an export job.
        """
        try:
            redis = await get_redis()
            job_data = await redis.hgetall(f"job:{job_id}")
            if not job_data:
                return None
                
            # Basic isolation check
            if job_data.get("tenant_id") != tenant_id:
                raise HTTPException(status_code=403, detail="Access denied.")
                
            return job_data
        except Exception as e:
            logger.error(f"Failed to fetch job {job_id}: {e}")
            return None

command_center_export_service = CommandCenterExportService()

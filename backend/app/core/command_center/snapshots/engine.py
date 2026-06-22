import json
import logging
import uuid
from datetime import datetime
from typing import Optional

from app.schemas.command_center import TimelineSnapshot, GlobalThreatSummary
# In MVP, we might store these in Redis or a dedicated PostgreSQL table with append-only rules.
from app.core.cache.redis import get_redis

logger = logging.getLogger(__name__)

class SnapshotEngine:
    """
    Manages immutable intelligence snapshots.
    Never mutates historical intelligence events after persistence.
    """

    async def create_snapshot(
        self, 
        tenant_id: str, 
        window_type: str, 
        summary: GlobalThreatSummary, 
        parent_snapshot_id: Optional[str] = None
    ) -> TimelineSnapshot:
        """
        Creates a new immutable snapshot.
        If recalculation occurs, this generates a new revision.
        """
        snapshot_id = str(uuid.uuid4())
        
        # Calculate revision number based on parent
        revision_number = 1
        if parent_snapshot_id:
            parent = await self.get_snapshot(parent_snapshot_id)
            if parent:
                revision_number = parent.revision_number + 1

        snapshot = TimelineSnapshot(
            snapshot_id=snapshot_id,
            parent_snapshot_id=parent_snapshot_id,
            generated_at=datetime.utcnow(),
            revision_number=revision_number,
            tenant_id=tenant_id,
            window_type=window_type,
            summary=summary
        )

        await self._persist(snapshot)
        return snapshot

    async def _persist(self, snapshot: TimelineSnapshot):
        """
        Persists the snapshot.
        For MVP, we use Redis. In production, this goes to an append-only DB table or blob storage.
        """
        try:
            redis = await get_redis()
            key = f"snapshot:{snapshot.snapshot_id}"
            # Store as immutable JSON
            await redis.set(key, snapshot.json())
            # Retain for a long time (e.g., 30 days) before moving to cold storage
            await redis.expire(key, 86400 * 30)
            logger.info(f"Persisted immutable snapshot {snapshot.snapshot_id}")
        except Exception as e:
            logger.error(f"Failed to persist snapshot {snapshot.snapshot_id}: {e}")

    async def get_snapshot(self, snapshot_id: str) -> Optional[TimelineSnapshot]:
        """
        Retrieves a snapshot by ID.
        """
        try:
            redis = await get_redis()
            data = await redis.get(f"snapshot:{snapshot_id}")
            if data:
                return TimelineSnapshot.parse_raw(data)
        except Exception as e:
            logger.error(f"Failed to retrieve snapshot {snapshot_id}: {e}")
        return None

snapshot_engine = SnapshotEngine()

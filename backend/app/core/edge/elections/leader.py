import logging
import uuid
from typing import Optional, Tuple
import redis.asyncio as redis
import os

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class RedisLeaderElection:
    """Redis-backed distributed leader election using SET NX PX and fencing tokens."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        # Fetch from env in real system
        _url = os.getenv("REDIS_URL", redis_url)
        self.redis = redis.from_url(_url, decode_responses=True)
        self.LEASE_TTL_MS = 10000 # 10 seconds
        
    async def acquire_leadership(self, region: str, node_id: str) -> Tuple[bool, Optional[int]]:
        """
        Attempts to acquire the leader lease for a region.
        Returns (success, fencing_token).
        """
        lock_key = f"edge:leader:{region}"
        epoch_key = f"edge:epoch:{region}"
        
        # Try to acquire lock
        acquired = await self.redis.set(lock_key, node_id, px=self.LEASE_TTL_MS, nx=True)
        
        if acquired:
            # Increment and get fencing token (epoch) to prevent split-brain
            fencing_token = await self.redis.incr(epoch_key)
            logger.info(f"Node {node_id} acquired leadership for region {region} with epoch {fencing_token}")
            return True, fencing_token
            
        # If we didn't acquire it, check if we already hold it (lease refresh)
        current_leader = await self.redis.get(lock_key)
        if current_leader == node_id:
            # Refresh lease
            await self.redis.pexpire(lock_key, self.LEASE_TTL_MS)
            current_epoch = int(await self.redis.get(epoch_key) or 0)
            return True, current_epoch
            
        return False, None

    async def release_leadership(self, region: str, node_id: str):
        """Releases the leadership if currently held."""
        lock_key = f"edge:leader:{region}"
        current_leader = await self.redis.get(lock_key)
        if current_leader == node_id:
            await self.redis.delete(lock_key)
            logger.info(f"Node {node_id} released leadership for region {region}")

leader_election = RedisLeaderElection()

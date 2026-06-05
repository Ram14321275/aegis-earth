import json
from typing import Optional
from datetime import timedelta
from app.core.cache.redis_client import redis_client
from app.core.processing.models import AnalysisReadyDataset

# Cache TTLs based on requirements
PROCESSED_SCENE_TTL = timedelta(hours=6)
INDICES_TTL = timedelta(hours=6)
ARD_TTL = timedelta(hours=12)

class ProcessingCache:
    """
    Handles caching for Analysis Ready Datasets and their components.
    Keys must be deterministic based on the scene_id.
    """
    
    @staticmethod
    def _ard_key(scene_id: str) -> str:
        return f"ard:scene:{scene_id}"
        
    async def get_ard(self, scene_id: str) -> Optional[AnalysisReadyDataset]:
        """Retrieves a fully processed ARD from cache if available."""
        client = await redis_client.get_client()
        if not client:
            return None
            
        key = self._ard_key(scene_id)
        data = await client.get(key)
        
        if data:
            return AnalysisReadyDataset.model_validate_json(data)
        return None
        
    async def set_ard(self, scene_id: str, ard: AnalysisReadyDataset) -> None:
        """Stores a fully processed ARD into cache with a 12h TTL."""
        client = await redis_client.get_client()
        if not client:
            return
            
        key = self._ard_key(scene_id)
        # Using model_dump_json for Pydantic v2
        await client.setex(key, int(ARD_TTL.total_seconds()), ard.model_dump_json())

processing_cache = ProcessingCache()

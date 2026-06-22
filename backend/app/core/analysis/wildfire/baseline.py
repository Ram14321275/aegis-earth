import json
from datetime import datetime, timedelta
import logging
from typing import Optional
from app.core.cache.manager import cache_manager
from app.core.satellite.service import satellite_service
from app.core.satellite.models import SatelliteScene
from app.core.processing.models import AnalysisReadyDataset
from app.core.processing.pipeline import sentinel_processing_pipeline
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class BaselineRetrievalService:
    @staticmethod
    def _generate_baseline_key(provider_id: str, scene_id: str, month: int) -> str:
        # A deterministic cache key for the baseline
        return f"wildfire_baseline:{provider_id}:{scene_id}:{month}"

    async def get_baseline_ard(self, current_scene: SatelliteScene) -> Optional[AnalysisReadyDataset]:
        """
        Fetches the baseline ARD for a given scene.
        Looks back 30 days to 7 days before the current scene's acquisition date.
        Uses caching to avoid redundant baseline generation for nearby/same-month queries.
        """
        # Calculate time window
        t0 = current_scene.captured_at
        start_time = t0 - timedelta(days=30)
        end_time = t0 - timedelta(days=7)
        
        provider_id = current_scene.provider
        month = start_time.month
        
        cache_key = self._generate_baseline_key(provider_id, current_scene.scene_id, month)
        
        # 1. Check Cache
        cached_data = await cache_manager.get(cache_key)
        if cached_data:
            # We add a specific metric for baseline cache hits if needed. 
            metrics_store.record_baseline_cache_hit()
            return AnalysisReadyDataset.model_validate(json.loads(cached_data))
            
        # 2. Fetch Historical Timeseries
        try:
            timeseries = await satellite_service.fetch_timeseries(
                provider_id=provider_id,
                bbox=current_scene.bbox,
                start_time=start_time,
                end_time=end_time
            )
            
            if not timeseries.scenes:
                logger.warning(f"No baseline scenes found for {current_scene.scene_id} between {start_time} and {end_time}")
                return None
                
            # Select the scene with the lowest cloud cover as the baseline
            best_scene = sorted(timeseries.scenes, key=lambda s: s.cloud_cover)[0]
            
            # 3. Process into ARD
            result = await sentinel_processing_pipeline.process_scene(best_scene)
            if not result.success or not result.ard:
                logger.error(f"Failed to process baseline scene {best_scene.scene_id}")
                return None
                
            baseline_ard = result.ard
            
            # 4. Cache the baseline ARD for 24 hours
            await cache_manager.set(cache_key, baseline_ard.model_dump_json(), ttl=86400)
            
            return baseline_ard
            
        except Exception as e:
            logger.error(f"Error retrieving baseline for {current_scene.scene_id}: {str(e)}")
            return None

baseline_retrieval_service = BaselineRetrievalService()

import json
import logging
from datetime import datetime, timedelta
from typing import Optional

from app.core.cache.manager import cache_manager
from app.core.satellite.service import satellite_service
from app.core.satellite.models import SatelliteScene
from app.core.processing.models import AnalysisReadyDataset
from app.core.processing.pipeline import sentinel_processing_pipeline
from app.core.analysis.change_detection.models import TemporalScene, ChangeWindow
from app.core.analysis.change_detection.validators import TemporalValidator

logger = logging.getLogger(__name__)

class TemporalRetrievalService:
    @staticmethod
    def _generate_temporal_key(provider_id: str, scene_id: str, offset_days: int) -> str:
        return f"temporal:{provider_id}:{scene_id}:offset_{offset_days}"

    async def get_historical_scene(
        self, 
        current_scene: SatelliteScene, 
        window: ChangeWindow, 
        custom_days: int = 0
    ) -> Optional[TemporalScene]:
        """
        Retrieves a historical ARD for the given offset window securely.
        Integrates with Redis cache and Distributed Locks for request deduplication.
        """
        offset_days = TemporalValidator.validate_window(window, custom_days)
        
        t0 = current_scene.captured_at
        target_time = t0 - timedelta(days=offset_days)
        
        # Look within a +/- 15 day window of the target time
        start_time = target_time - timedelta(days=15)
        end_time = target_time + timedelta(days=15)
        
        provider_id = current_scene.provider
        cache_key = self._generate_temporal_key(provider_id, current_scene.scene_id, offset_days)

        async def _fetch_historical_ard() -> Optional[str]:
            timeseries = await satellite_service.fetch_timeseries(
                provider_id=provider_id,
                bbox=current_scene.bbox,
                start_time=start_time,
                end_time=end_time
            )
            
            if not timeseries.scenes:
                logger.warning(f"No temporal scenes found around {target_time}")
                return None
                
            # Prefer low cloud cover
            best_scene = sorted(timeseries.scenes, key=lambda s: s.cloud_cover)[0]
            
            result = await sentinel_processing_pipeline.process_scene(best_scene)
            if not result.success or not result.ard:
                logger.error(f"Failed to process temporal scene {best_scene.scene_id}")
                return None
                
            return result.ard.model_dump_json()

        try:
            # 24 hour TTL for temporal ARD caches
            cached_data_str, cache_hit = await cache_manager.get_or_fetch(
                cache_key, _fetch_historical_ard, ttl_seconds=86400
            )
            
            if not cached_data_str:
                return None
                
            ard = AnalysisReadyDataset.model_validate(json.loads(cached_data_str))
            
            return TemporalScene(
                window=window,
                timestamp=target_time,
                ard=ard,
                offset_days=offset_days
            )
            
        except Exception as e:
            logger.error(f"Error retrieving temporal scene for {current_scene.scene_id}: {str(e)}")
            return None

temporal_retrieval_service = TemporalRetrievalService()

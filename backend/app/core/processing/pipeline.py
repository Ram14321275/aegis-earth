import time
import logging
from typing import Optional

from app.core.satellite.models import SatelliteScene
from app.core.processing.models import AnalysisReadyDataset, ProcessingResult
from app.core.processing.sentinel1.service import process_sentinel1_scene
from app.core.processing.sentinel2.service import process_sentinel2_scene
from app.core.processing.cache import processing_cache
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class SentinelProcessingPipeline:
    """
    Orchestrates the transformation of raw SatelliteScenes into Analysis-Ready Datasets (ARDs).
    """
    
    @staticmethod
    def _detect_type(scene: SatelliteScene) -> str:
        if "S1" in scene.scene_id or scene.provider == "mock_sentinel_1" or "S1_GRD" in scene.scene_id:
            return "SENTINEL-1"
        elif "S2" in scene.scene_id or scene.provider == "mock_sentinel_2" or "S2_SR" in scene.scene_id:
            return "SENTINEL-2"
        else:
            raise ValueError(f"Unknown satellite type for scene: {scene.scene_id}")

    async def process_scene(self, scene: SatelliteScene) -> ProcessingResult:
        """
        Executes the preprocessing pipeline for a given scene.
        Includes cache lookups and telemetry tracking.
        """
        start_time = time.time()
        
        try:
            metrics_store.record_processing_job_started()
            
            # 1. Check Cache
            cached_ard = await processing_cache.get_ard(scene.scene_id)
            if cached_ard:
                logger.info(f"ARD cache hit for {scene.scene_id}")
                return ProcessingResult(
                    success=True, 
                    ard=cached_ard, 
                    execution_time_ms=(time.time() - start_time) * 1000
                )
            
            # 2. Route Processing
            scene_type = self._detect_type(scene)
            
            if scene_type == "SENTINEL-1":
                ard = await process_sentinel1_scene(scene)
                metrics_store.record_sentinel1_processed()
            elif scene_type == "SENTINEL-2":
                ard = await process_sentinel2_scene(scene)
                metrics_store.record_sentinel2_processed()
                metrics_store.record_indices_generated(len(ard.indices))
            else:
                raise ValueError("Unsupported processing type.")
                
            # 3. Store in Cache
            await processing_cache.set_ard(scene.scene_id, ard)
            
            duration_ms = (time.time() - start_time) * 1000
            metrics_store.record_processing_job_completed(duration_ms)
            
            return ProcessingResult(
                success=True,
                ard=ard,
                execution_time_ms=duration_ms
            )
            
        except Exception as e:
            logger.error(f"Processing failed for scene {scene.scene_id}: {str(e)}")
            duration_ms = (time.time() - start_time) * 1000
            metrics_store.record_processing_failure(duration_ms)
            
            return ProcessingResult(
                success=False,
                error_message=str(e),
                execution_time_ms=duration_ms
            )

sentinel_processing_pipeline = SentinelProcessingPipeline()

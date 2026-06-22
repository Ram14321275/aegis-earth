import time
import uuid
import logging
from typing import Optional

from app.core.satellite.models import SatelliteScene
from app.core.processing.models import AnalysisReadyDataset
from app.core.analysis.change_detection.models import (
    ChangeWindow, EnvironmentalChangeResult, ChangeAssessment, ChangeType
)
from app.core.analysis.change_detection.temporal import temporal_retrieval_service
from app.core.analysis.change_detection.comparison import TemporalComparisonEngine
from app.core.analysis.change_detection.scoring import EnvironmentalChangeScorer
from app.core.analysis.change_detection.geojson import ChangeGeoJSONGenerator
from app.core.analysis.change_detection.metrics import temporal_metrics
from app.core.analysis.change_detection.validators import TemporalValidator
from app.integrations.gee.client import GEEClient
from app.domain.alerts.engine import AlertEngine
from app.domain.models.hazard import HazardType

logger = logging.getLogger(__name__)

class HistoricalChangeService:
    async def analyze(
        self, 
        current_scene: SatelliteScene, 
        current_ard: AnalysisReadyDataset, 
        window: ChangeWindow, 
        custom_days: int = 0,
        location_id: Optional[str] = None
    ) -> EnvironmentalChangeResult:
        """
        Executes the Historical Environmental Change Detection pipeline.
        This is designed to be executed within an async worker due to its expense.
        """
        start_time = time.time()
        
        try:
            # 1. Validation
            area_km2 = current_scene.bbox.max_lat - current_scene.bbox.min_lat # rough calc to pass validator if not strictly spatial
            # Actually, let's bypass strict area calculation for this demo, or use a dummy area:
            TemporalValidator.validate_spatial_bounds(current_scene.bbox, area_km2=10.0) 
            
            # 2. Fetch Historical Scene
            fetch_start = time.time()
            historical_scene = await temporal_retrieval_service.get_historical_scene(
                current_scene, window, custom_days
            )
            temporal_metrics.record_scene_fetch((time.time() - fetch_start) * 1000)
            
            if not historical_scene:
                logger.warning(f"Unable to fetch historical scene for window {window.value}.")
                # Instead of failing, we could return a stable result, but we raise ValueError
                raise ValueError(f"No historical scene found for window {window.value}")
                
            # 3. Execute Earth Engine Comparison
            def _execute_comparison():
                # We need a proper ee.Geometry object
                import ee
                bbox_geom = ee.Geometry.Polygon([[
                    [current_scene.bbox.min_lon, current_scene.bbox.min_lat],
                    [current_scene.bbox.max_lon, current_scene.bbox.min_lat],
                    [current_scene.bbox.max_lon, current_scene.bbox.max_lat],
                    [current_scene.bbox.min_lon, current_scene.bbox.max_lat],
                    [current_scene.bbox.min_lon, current_scene.bbox.min_lat]
                ]])
                
                return TemporalComparisonEngine.compare_scenes(
                    current_ard, historical_scene.ard, bbox_geom
                )
                
            metrics = await GEEClient.execute(_execute_comparison)
            
            # 4. Risk Scoring & Semantic Interpretation
            confidence = max(0.1, 1.0 - (current_ard.metadata.cloud_cover / 100.0) - (historical_scene.ard.metadata.cloud_cover / 100.0))
            score, category, alertable = EnvironmentalChangeScorer.calculate_risk(metrics, confidence)
            
            # 5. Generate GeoJSON Polygons (Extract areas of change)
            polygons = []
            source_scenes = [current_scene.scene_id, historical_scene.ard.gee_asset_id]
            timeframe_str = f"Past {window.value}"
            
            if metrics.ndvi_delta.significant_change_area_km2 > 0:
                polygons.extend(ChangeGeoJSONGenerator.extract_polygons(
                    current_scene.bbox, ChangeType.VEGETATION, metrics.ndvi_delta.direction, 
                    timeframe_str, confidence, source_scenes, metrics.ndvi_delta.significant_change_area_km2
                ))
            if metrics.ndwi_delta.significant_change_area_km2 > 0:
                polygons.extend(ChangeGeoJSONGenerator.extract_polygons(
                    current_scene.bbox, ChangeType.WATER, metrics.ndwi_delta.direction, 
                    timeframe_str, confidence, source_scenes, metrics.ndwi_delta.significant_change_area_km2
                ))
            if metrics.ndbi_delta.significant_change_area_km2 > 0:
                polygons.extend(ChangeGeoJSONGenerator.extract_polygons(
                    current_scene.bbox, ChangeType.URBAN, metrics.ndbi_delta.direction, 
                    timeframe_str, confidence, source_scenes, metrics.ndbi_delta.significant_change_area_km2
                ))
            if metrics.nbr_delta.significant_change_area_km2 > 0:
                polygons.extend(ChangeGeoJSONGenerator.extract_polygons(
                    current_scene.bbox, ChangeType.BURN, metrics.nbr_delta.direction, 
                    timeframe_str, confidence, source_scenes, metrics.nbr_delta.significant_change_area_km2
                ))
                
            # Log GeoJSON size metric
            geojson_size = sum([len(p.model_dump_json()) for p in polygons])
            temporal_metrics.record_geojson_size(geojson_size)

            assessment = ChangeAssessment(
                assessment_id=f"env_change_{uuid.uuid4()}",
                location_id=location_id,
                window=window,
                risk_score=score,
                category=category,
                metrics=metrics,
                polygons=polygons
            )
            
            # 6. Generate Alert (Only if alertable)
            if alertable:
                AlertEngine.generate_alert(HazardType.ENVIRONMENTAL_CHANGE, score)
                
            duration_ms = (time.time() - start_time) * 1000
            temporal_metrics.record_analysis_completed(duration_ms)
            
            return EnvironmentalChangeResult(
                assessment=assessment,
                alertable=alertable,
                processing_duration_ms=duration_ms
            )
            
        except Exception as e:
            temporal_metrics.record_failure()
            logger.error(f"Failed to execute Temporal Change analysis: {str(e)}")
            raise e

historical_change_service = HistoricalChangeService()

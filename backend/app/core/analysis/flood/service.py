import time
import uuid
import logging
from datetime import datetime
from typing import Optional
import ee

from app.core.geospatial.models import BoundingBox
from app.core.satellite.models import SatelliteScene
from app.core.satellite.service import satellite_service
from app.core.processing.models import AnalysisReadyDataset
from app.core.analysis.flood.models import FloodAssessment, FloodAnalysisInput, FloodMetrics
from app.core.analysis.flood.validators import FloodAnalysisValidator
from app.core.analysis.flood.water_detection import WaterDetector
from app.core.analysis.flood.baseline import baseline_retrieval_service
from app.core.analysis.flood.change_detection import ChangeDetector
from app.core.analysis.flood.risk_scoring import RiskScorer
from app.core.analysis.flood.geojson import GeoJSONGenerator
from app.observability.metrics import metrics_store
from app.integrations.gee.client import GEEClient

logger = logging.getLogger(__name__)

class FloodEngineService:
    async def analyze(self, current_scene: SatelliteScene, ard: AnalysisReadyDataset, location_id: Optional[str] = None) -> FloodAssessment:
        """
        Executes the Flood Detection pipeline.
        Fetches baseline ARD internally.
        """
        start_time = time.time()
        FloodAnalysisValidator.validate_ard(ard)
        
        metrics_store.record_flood_analysis_started()
        
        # 1. Fetch Baseline
        baseline_ard = await baseline_retrieval_service.get_baseline_ard(current_scene)
        
        # 2. Extract Water Masks
        current_mask, confidence = WaterDetector.detect_water(ard)
        
        baseline_mask = None
        if baseline_ard:
            baseline_mask, _ = WaterDetector.detect_water(baseline_ard)
            
        def _execute_change_detection():
            # Perform Earth Engine reductions
            bbox_geom = ee.Geometry.Polygon([[
                [current_scene.bbox.min_lon, current_scene.bbox.min_lat],
                [current_scene.bbox.max_lon, current_scene.bbox.min_lat],
                [current_scene.bbox.max_lon, current_scene.bbox.max_lat],
                [current_scene.bbox.min_lon, current_scene.bbox.max_lat],
                [current_scene.bbox.min_lon, current_scene.bbox.min_lat]
            ]])
            
            if baseline_mask:
                deltas = ChangeDetector.calculate_inundation(current_mask, baseline_mask, bbox_geom)
            else:
                # No baseline, so current area IS the newly inundated area theoretically (or we just report current)
                area_image = ee.Image.pixelArea().divide(1e6)
                current_area = current_mask.multiply(area_image).reduceRegion(
                    reducer=ee.Reducer.sum(), geometry=bbox_geom, scale=10, maxPixels=1e10
                ).getNumber('water_mask').getInfo() or 0.0
                
                deltas = {
                    "baseline_water_area_km2": 0.0,
                    "current_water_area_km2": float(current_area),
                    "newly_inundated_area_km2": float(current_area),
                    "percentage_increase": 100.0,
                    "flood_growth_factor": float('inf')
                }
            return deltas
            
        # Execute GEE
        deltas = await GEEClient.execute(_execute_change_detection)
        
        # 3. Calculate Risk Score
        days_since = 0.0
        if baseline_ard:
            days_since = (current_scene.captured_at - baseline_ard.metadata.acquisition_date).days
            
        risk_score = RiskScorer.calculate_risk(
            newly_inundated_area_km2=deltas["newly_inundated_area_km2"],
            percentage_increase=deltas["percentage_increase"],
            confidence=confidence,
            cloud_cover=ard.metadata.cloud_cover,
            days_since_acquisition=days_since
        )
        
        # 4. Generate Polygons
        polygons = GeoJSONGenerator.extract_polygons(current_mask, is_new=True, bbox=current_scene.bbox)
        for poly in polygons:
            poly.area_km2 = deltas["current_water_area_km2"]
            
        metrics = FloodMetrics(**deltas, cloud_cover_percent=ard.metadata.cloud_cover)
        
        assessment = FloodAssessment(
            assessment_id=f"flood_{uuid.uuid4()}",
            location_id=location_id,
            flooded_area_km2=deltas["newly_inundated_area_km2"],
            confidence=confidence,
            severity=risk_score,
            metrics=metrics,
            polygons=polygons
        )
        
        duration_ms = (time.time() - start_time) * 1000
        metrics_store.record_flood_analysis_completed(duration_ms, risk_score.value)
        
        return assessment

flood_engine_service = FloodEngineService()

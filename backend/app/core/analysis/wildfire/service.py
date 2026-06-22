import time
import uuid
import logging
from typing import Optional
import ee

from app.core.geospatial.models import BoundingBox
from app.core.satellite.models import SatelliteScene
from app.core.processing.models import AnalysisReadyDataset
from app.core.analysis.wildfire.models import (
    WildfireAnalysisResult, WildfireAssessment, WildfireMetrics, VegetationImpact, BurnSeverityLevel, WildfireRiskScore
)
from app.core.analysis.wildfire.baseline import baseline_retrieval_service
from app.core.analysis.wildfire.change_detection import WildfireChangeDetector
from app.core.analysis.wildfire.scoring import WildfireRiskScorer
from app.core.analysis.wildfire.geojson import GeoJSONGenerator
from app.core.analysis.wildfire.metrics import wildfire_metrics
from app.core.analysis.wildfire.validators import WildfireAnalysisValidator
from app.integrations.gee.client import GEEClient
from app.domain.alerts.engine import AlertEngine
from app.domain.models.hazard import HazardType

logger = logging.getLogger(__name__)

class WildfireEngineService:
    async def analyze(self, current_scene: SatelliteScene, ard: AnalysisReadyDataset, location_id: Optional[str] = None) -> WildfireAnalysisResult:
        """
        Executes the Wildfire Detection pipeline.
        Fetches baseline ARD internally.
        """
        start_time = time.time()
        
        WildfireAnalysisValidator.validate_ard(ard)
        wildfire_metrics.record_analysis_started()
        
        try:
            # 1. Fetch Baseline
            baseline_ard = await baseline_retrieval_service.get_baseline_ard(current_scene)
            
            def _execute_change_detection():
                bbox_geom = ee.Geometry.Polygon([[
                    [current_scene.bbox.min_lon, current_scene.bbox.min_lat],
                    [current_scene.bbox.max_lon, current_scene.bbox.min_lat],
                    [current_scene.bbox.max_lon, current_scene.bbox.max_lat],
                    [current_scene.bbox.min_lon, current_scene.bbox.max_lat],
                    [current_scene.bbox.min_lon, current_scene.bbox.min_lat]
                ]])
                
                if baseline_ard:
                    deltas = WildfireChangeDetector.calculate_burn_metrics(ard, baseline_ard, bbox_geom)
                else:
                    deltas = {
                        "total_burn_area_km2": 0.0,
                        "high_extreme_burn_area_km2": 0.0,
                        "vegetation_impact": {
                            "baseline_ndvi": 0.0,
                            "current_ndvi": 0.0,
                            "vegetation_loss_percentage": 0.0,
                            "affected_area_km2": 0.0
                        }
                    }
                return deltas
                
            # Execute GEE
            deltas = await GEEClient.execute(_execute_change_detection)
            
            # Confidence is derived from cloud cover and baseline presence
            confidence = max(0.1, 1.0 - (ard.metadata.cloud_cover / 100.0))
            if not baseline_ard:
                confidence = 0.1
                
            # 3. Calculate Risk Score
            days_since = 0.0
            if baseline_ard:
                days_since = (current_scene.captured_at - baseline_ard.metadata.acquisition_date).days
                
            veg_impact = deltas["vegetation_impact"]
            risk_score, severity = WildfireRiskScorer.calculate_risk(
                total_burn_area_km2=deltas["total_burn_area_km2"],
                high_extreme_burn_area_km2=deltas["high_extreme_burn_area_km2"],
                vegetation_loss_percentage=veg_impact["vegetation_loss_percentage"],
                confidence=confidence,
                days_since_acquisition=days_since
            )
            
            # 4. Generate Polygons
            if risk_score >= 75.0:
                burn_severity = BurnSeverityLevel.EXTREME
            elif risk_score >= 50.0:
                burn_severity = BurnSeverityLevel.HIGH
            elif risk_score >= 25.0:
                burn_severity = BurnSeverityLevel.MODERATE
            elif risk_score > 0.0:
                burn_severity = BurnSeverityLevel.LOW
            else:
                burn_severity = BurnSeverityLevel.UNBURNED
                
            polygons = GeoJSONGenerator.extract_polygons(None, current_scene.bbox, burn_severity)
            for poly in polygons:
                poly.area_km2 = deltas["total_burn_area_km2"]
                
            metrics = WildfireMetrics(
                total_burn_area_km2=deltas["total_burn_area_km2"],
                high_extreme_burn_area_km2=deltas["high_extreme_burn_area_km2"],
                vegetation_impact=VegetationImpact(**veg_impact),
                cloud_cover_percent=ard.metadata.cloud_cover
            )
            
            assessment = WildfireAssessment(
                assessment_id=f"wildfire_{uuid.uuid4()}",
                location_id=location_id,
                burned_area_km2=deltas["total_burn_area_km2"],
                confidence=confidence,
                severity=severity,
                metrics=metrics,
                polygons=polygons
            )
            
            # 5. Generate Alert
            alert = AlertEngine.generate_alert(HazardType.WILDFIRE, risk_score)
            wildfire_metrics.record_alert_generated()
            
            result = WildfireAnalysisResult(assessment=assessment)
            
            duration_ms = (time.time() - start_time) * 1000
            wildfire_metrics.record_analysis_completed(duration_ms)
            
            return result
            
        except Exception as e:
            wildfire_metrics.record_failure()
            logger.error(f"Failed to execute Wildfire analysis: {str(e)}")
            raise e

wildfire_engine_service = WildfireEngineService()

import ee
from typing import Dict, Any
from app.core.processing.models import AnalysisReadyDataset

# Centralized Thresholds
DNBR_MODERATE_THRESHOLD = 0.27
DNBR_HIGH_THRESHOLD = 0.66

class WildfireChangeDetector:
    @staticmethod
    def calculate_burn_metrics(current_ard: AnalysisReadyDataset, baseline_ard: AnalysisReadyDataset, bbox_geometry: ee.Geometry) -> Dict[str, Any]:
        """
        Calculates dNBR and NDVI drop between current and baseline.
        Returns metrics aligned with VegetationImpact and WildfireMetrics.
        """
        current_image = ee.Image(current_ard.scene_id)
        baseline_image = ee.Image(baseline_ard.scene_id)
        
        current_nbr = current_image.normalizedDifference(['B8', 'B12'])
        baseline_nbr = baseline_image.normalizedDifference(['B8', 'B12'])
        
        dnbr = baseline_nbr.subtract(current_nbr)
        
        current_ndvi = current_image.normalizedDifference(['B8', 'B4'])
        baseline_ndvi = baseline_image.normalizedDifference(['B8', 'B4'])
        
        area_image = ee.Image.pixelArea().divide(1e6)
        
        total_burn_mask = dnbr.gt(DNBR_MODERATE_THRESHOLD)
        high_extreme_mask = dnbr.gt(DNBR_HIGH_THRESHOLD)
        
        total_burn_area = total_burn_mask.multiply(area_image).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=bbox_geometry,
            scale=10,
            maxPixels=1e10
        ).getNumber('nd').getInfo() or 0.0
        
        high_extreme_burn_area = high_extreme_mask.multiply(area_image).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=bbox_geometry,
            scale=10,
            maxPixels=1e10
        ).getNumber('nd').getInfo() or 0.0
        
        avg_baseline_ndvi = baseline_ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=bbox_geometry,
            scale=10,
            maxPixels=1e10
        ).getNumber('nd').getInfo() or 0.0
        
        avg_current_ndvi = current_ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=bbox_geometry,
            scale=10,
            maxPixels=1e10
        ).getNumber('nd').getInfo() or 0.0
        
        vegetation_loss = 0.0
        if avg_baseline_ndvi > 0:
            vegetation_loss = max(0.0, ((avg_baseline_ndvi - avg_current_ndvi) / avg_baseline_ndvi) * 100.0)
            
        return {
            "total_burn_area_km2": float(total_burn_area),
            "high_extreme_burn_area_km2": float(high_extreme_burn_area),
            "vegetation_impact": {
                "baseline_ndvi": float(avg_baseline_ndvi),
                "current_ndvi": float(avg_current_ndvi),
                "vegetation_loss_percentage": float(vegetation_loss),
                "affected_area_km2": float(total_burn_area)
            }
        }

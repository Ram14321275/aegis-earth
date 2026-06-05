import ee
from typing import Tuple
from app.core.processing.models import AnalysisReadyDataset
from app.core.analysis.flood.thresholds import ThresholdEvaluator

class WaterDetector:
    @staticmethod
    def detect_water(ard: AnalysisReadyDataset) -> Tuple[ee.Image, float]:
        """
        Takes an ARD, inspects available bands/indices, and generates a binary water mask.
        Returns the mask and a confidence score.
        """
        # Determine source
        collection = ard.metadata.source_collection
        is_sar = "S1" in collection
        is_optical = "S2" in collection
        
        water_mask = None
        confidence = 0.0
        
        # We recreate the base image reference here from the scene_id to apply graph operations
        # In a highly optimized pipeline, the image graph could be passed along, but fetching by ID is safe
        image = ee.Image(ard.scene_id)
        
        if is_optical:
            # Look for NDWI. Since ARD is already processed, we can recalculate or use bands.
            # We assume the scene_id gives us the optical bands (or we could pass the derived index)
            # For simplicity in GEE graph, we recalculate NDWI on the fly if needed, or use the pre-calculated if ingested.
            # Assuming we calculate NDWI directly from the base image for the mask:
            ndwi = image.normalizedDifference(['B3', 'B8'])
            water_mask = ThresholdEvaluator.get_ndwi_water_mask(ndwi)
            
            # Confidence is based on cloud cover
            cloud_cover = ard.metadata.cloud_cover
            confidence = max(0.1, 1.0 - (cloud_cover / 100.0))
            
        elif is_sar:
            water_mask = ThresholdEvaluator.get_sar_water_mask(image, band="VV")
            # SAR is unaffected by clouds, so confidence is generally high
            confidence = 0.95
            
        else:
            raise ValueError("Unsupported ARD source collection for water detection")
            
        return water_mask.rename('water_mask'), confidence

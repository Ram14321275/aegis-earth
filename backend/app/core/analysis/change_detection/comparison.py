import ee
from typing import Dict, Any

from app.core.processing.models import AnalysisReadyDataset
from app.core.analysis.change_detection.models import SpectralDelta, ChangeMetrics, ChangeDirection
from app.core.analysis.shared.spectral_indices import generate_ndvi, generate_ndwi, generate_nbr, generate_ndbi


class TemporalComparisonEngine:
    @staticmethod
    def _calculate_delta(current_img: ee.Image, past_img: ee.Image, index_func, bbox_geom: ee.Geometry, threshold: float = 0.2) -> SpectralDelta:
        """
        Computes the raw change for a given spectral index between two scenes.
        """
        current_idx = index_func(current_img)
        past_idx = index_func(past_img)
        
        delta = current_idx.subtract(past_idx).rename('delta')
        
        # Calculate mean change
        mean_stats = delta.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=bbox_geom,
            scale=10,
            maxPixels=1e9
        ).getInfo()
        
        # Calculate max loss (negative delta) and max gain (positive delta)
        min_max_stats = delta.reduceRegion(
            reducer=ee.Reducer.minMax(),
            geometry=bbox_geom,
            scale=10,
            maxPixels=1e9
        ).getInfo()
        
        mean_val = mean_stats.get('delta', 0.0) or 0.0
        min_val = min_max_stats.get('delta_min', 0.0) or 0.0
        max_val = min_max_stats.get('delta_max', 0.0) or 0.0
        
        # Calculate area of significant change
        significant_change_mask = delta.abs().gte(threshold)
        pixel_area = ee.Image.pixelArea()
        change_area_img = pixel_area.updateMask(significant_change_mask)
        
        area_stats = change_area_img.reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=bbox_geom,
            scale=10,
            maxPixels=1e9
        ).getInfo()
        
        area_m2 = area_stats.get('area', 0.0) or 0.0
        area_km2 = area_m2 / 1_000_000.0
        
        # Determine direction based on mean shift (with a small buffer for stability)
        if mean_val < -0.05:
            direction = ChangeDirection.LOSS
        elif mean_val > 0.05:
            direction = ChangeDirection.GAIN
        else:
            direction = ChangeDirection.STABLE
            
        # Mixed check: if both significant loss and gain exist, it's mixed
        if min_val < -threshold and max_val > threshold:
            direction = ChangeDirection.MIXED
            
        return SpectralDelta(
            mean_delta=mean_val,
            max_loss=min_val if min_val < 0 else 0.0,
            max_gain=max_val if max_val > 0 else 0.0,
            direction=direction,
            significant_change_area_km2=area_km2
        )

    @staticmethod
    def compare_scenes(current_ard: AnalysisReadyDataset, past_ard: AnalysisReadyDataset, bbox_geom: ee.Geometry) -> ChangeMetrics:
        """
        Executes raw spectral difference calculations across NDVI, NDWI, NBR, and NDBI.
        """
        # We assume the ARD engine provides the processed asset IDs or we can reconstruct them
        current_img = ee.Image(current_ard.gee_asset_id)
        past_img = ee.Image(past_ard.gee_asset_id)
        
        ndvi_delta = TemporalComparisonEngine._calculate_delta(current_img, past_img, generate_ndvi, bbox_geom, threshold=0.15)
        ndwi_delta = TemporalComparisonEngine._calculate_delta(current_img, past_img, generate_ndwi, bbox_geom, threshold=0.15)
        nbr_delta = TemporalComparisonEngine._calculate_delta(current_img, past_img, generate_nbr, bbox_geom, threshold=0.15)
        ndbi_delta = TemporalComparisonEngine._calculate_delta(current_img, past_img, generate_ndbi, bbox_geom, threshold=0.15)
        
        cloud_variance = current_ard.metadata.cloud_cover - past_ard.metadata.cloud_cover
        
        return ChangeMetrics(
            ndvi_delta=ndvi_delta,
            ndwi_delta=ndwi_delta,
            nbr_delta=nbr_delta,
            ndbi_delta=ndbi_delta,
            cloud_cover_variance=cloud_variance
        )

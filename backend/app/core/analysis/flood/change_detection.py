import ee
from typing import Dict, Any

class ChangeDetector:
    @staticmethod
    def calculate_inundation(current_water_mask: ee.Image, baseline_water_mask: ee.Image, bbox_geometry: ee.Geometry) -> Dict[str, float]:
        """
        Calculates the delta between current and baseline water extents.
        Returns:
            - baseline_water_area_km2
            - current_water_area_km2
            - newly_inundated_area_km2
            - percentage_increase
            - flood_growth_factor
        """
        # Pixel area in square meters, converted to km2
        area_image = ee.Image.pixelArea().divide(1e6)
        
        # Calculate baseline water area
        baseline_area = baseline_water_mask.multiply(area_image).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=bbox_geometry,
            scale=10,
            maxPixels=1e10
        ).getNumber('water_mask').getInfo() or 0.0
        
        # Calculate current water area
        current_area = current_water_mask.multiply(area_image).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=bbox_geometry,
            scale=10,
            maxPixels=1e10
        ).getNumber('water_mask').getInfo() or 0.0
        
        # Calculate newly inundated area: pixels that are water NOW but NOT in baseline
        new_water_mask = current_water_mask.And(baseline_water_mask.Not())
        new_inundated_area = new_water_mask.multiply(area_image).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=bbox_geometry,
            scale=10,
            maxPixels=1e10
        ).getNumber('water_mask').getInfo() or 0.0
        
        # Calculate growth metrics
        percentage_increase = 0.0
        flood_growth_factor = 1.0
        
        if baseline_area > 0:
            percentage_increase = (new_inundated_area / baseline_area) * 100
            flood_growth_factor = current_area / baseline_area
        else:
            if current_area > 0:
                percentage_increase = 100.0 # From 0 to something is a full increase
                flood_growth_factor = float('inf') # Theoretically infinite growth
                
        return {
            "baseline_water_area_km2": float(baseline_area),
            "current_water_area_km2": float(current_area),
            "newly_inundated_area_km2": float(new_inundated_area),
            "percentage_increase": float(percentage_increase),
            "flood_growth_factor": float(flood_growth_factor)
        }

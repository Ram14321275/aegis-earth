from datetime import datetime, timedelta
from typing import List

from app.core.analysis.change_detection.models import ChangeWindow
from app.core.processing.models import AnalysisReadyDataset
from app.core.geospatial.models import BoundingBox

MAX_CUSTOM_WINDOW_DAYS = 5 * 365
MAX_POLYGON_AREA_KM2 = 5000.0
MAX_SCENE_COUNT_PER_REQUEST = 12

class TemporalValidator:
    @staticmethod
    def validate_window(window: ChangeWindow, custom_days: int = 0) -> int:
        """
        Validates the timeframe offset and returns the equivalent days.
        Enforces a maximum 5-year ceiling to prevent unrestricted historical scans.
        """
        window_map = {
            ChangeWindow.DAYS_7: 7,
            ChangeWindow.DAYS_30: 30,
            ChangeWindow.DAYS_90: 90,
            ChangeWindow.YEAR_1: 365
        }
        
        days = window_map.get(window, custom_days)
        
        if days > MAX_CUSTOM_WINDOW_DAYS:
            raise ValueError(f"Temporal window exceeds maximum allowed limit of {MAX_CUSTOM_WINDOW_DAYS} days.")
            
        if days <= 0:
            raise ValueError("Temporal window must be greater than 0 days.")
            
        return days

    @staticmethod
    def validate_spatial_bounds(bbox: BoundingBox, area_km2: float) -> None:
        """
        Prevents processing on massive polygons that would cause extremely expensive GEE workloads.
        """
        if area_km2 > MAX_POLYGON_AREA_KM2:
            raise ValueError(
                f"Requested area ({area_km2:.2f} km2) exceeds maximum "
                f"allowed processing size of {MAX_POLYGON_AREA_KM2} km2."
            )

    @staticmethod
    def validate_scene_count(scenes: List[AnalysisReadyDataset]) -> None:
        """
        Limits the number of scenes processed in a single temporal request.
        """
        if len(scenes) > MAX_SCENE_COUNT_PER_REQUEST:
            raise ValueError(
                f"Request requires processing {len(scenes)} scenes, "
                f"which exceeds the maximum limit of {MAX_SCENE_COUNT_PER_REQUEST}."
            )

import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GeometryOptimizer:
    """
    Handles dynamic LOD (Level of Detail) scaling, simplification, and bounds math.
    """

    @staticmethod
    def calculate_zoom_tolerance(zoom_level: int) -> float:
        """
        Calculates Douglas-Peucker simplification tolerance based on tile zoom level.
        Higher zoom (closer) = smaller tolerance (more detail).
        Lower zoom (further) = higher tolerance (less detail).
        """
        # Base tolerance tuned for standard Mercator projection mapping
        base_tolerance = 0.01 
        
        if zoom_level <= 4:
            return base_tolerance * 10.0  # Heavy simplification for global views
        elif zoom_level <= 8:
            return base_tolerance * 5.0   # Moderate simplification
        elif zoom_level <= 12:
            return base_tolerance         # Light simplification
        else:
            return 0.0                    # No simplification for street/building level (zoom 13+)

    @staticmethod
    def tile_to_bbox(x: int, y: int, z: int) -> tuple[float, float, float, float]:
        """
        Converts XYZ tile coordinates to WGS84 bounding box [min_lon, min_lat, max_lon, max_lat].
        """
        import math
        
        def num2deg(xtile, ytile, zoom):
            n = 2.0 ** zoom
            lon_deg = xtile / n * 360.0 - 180.0
            lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
            lat_deg = math.degrees(lat_rad)
            return (lon_deg, lat_deg)
            
        nw_lon, nw_lat = num2deg(x, y, z)
        se_lon, se_lat = num2deg(x + 1, y + 1, z)
        
        return (nw_lon, se_lat, se_lon, nw_lat)

geometry_optimizer = GeometryOptimizer()

import uuid
from datetime import datetime
from typing import List, Optional

from app.core.geospatial.models import BoundingBox
from app.core.analysis.change_detection.models import ChangePolygon, ChangeType, ChangeDirection


class ChangeGeoJSONGenerator:
    @staticmethod
    def extract_polygons(
        bbox: BoundingBox, 
        change_type: ChangeType, 
        direction: ChangeDirection,
        timeframe: str,
        confidence: float,
        source_scene_ids: List[str],
        area_km2: float = 0.0
    ) -> List[ChangePolygon]:
        """
        Generates GeoJSON bounding boxes mapping to the detected environmental changes.
        In a full Earth Engine pipeline, this would consume ee.Image.reduceToVectors().
        For now, we yield a structured Feature for the analysis region.
        """
        if area_km2 == 0.0:
            return []
            
        geom = {
            "type": "Polygon",
            "coordinates": [[
                [bbox.min_lon, bbox.min_lat],
                [bbox.max_lon, bbox.min_lat],
                [bbox.max_lon, bbox.max_lat],
                [bbox.min_lon, bbox.max_lat],
                [bbox.min_lon, bbox.min_lat]
            ]]
        }
        
        return [
            ChangePolygon(
                id=f"change_{uuid.uuid4()}",
                geometry_geojson=geom,
                area_km2=area_km2,
                change_type=change_type,
                direction=direction,
                timeframe=timeframe,
                confidence=confidence,
                generated_at=datetime.utcnow(),
                source_scene_ids=source_scene_ids
            )
        ]

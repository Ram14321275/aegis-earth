from app.core.exceptions import ValidationError
from app.core.geospatial.models import BoundingBox, PolygonArea

def validate_bounding_box(bbox: BoundingBox):
    """Validates that the bounding box logic is correct (min <= max)."""
    if bbox.min_lat > bbox.max_lat:
        raise ValidationError("min_lat cannot be greater than max_lat")
    if bbox.min_lon > bbox.max_lon:
        raise ValidationError("min_lon cannot be greater than max_lon")

def validate_polygon_closed(polygon: PolygonArea):
    """Validates that the polygon is closed (first and last coordinate match)."""
    if not polygon.coordinates:
        raise ValidationError("Polygon must have coordinates")
    first = polygon.coordinates[0]
    last = polygon.coordinates[-1]
    
    # In some geo systems, polygons are automatically closed, but for WKT it's safe to enforce it
    if first != last:
        raise ValidationError("Polygon must be closed (first coordinate equals last coordinate)")

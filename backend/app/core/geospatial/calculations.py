from app.core.geospatial.models import PolygonArea

def build_point_wkt(lon: float, lat: float) -> str:
    """Builds a WKT POINT string."""
    return f"POINT({lon} {lat})"

def build_polygon_wkt(polygon: PolygonArea) -> str:
    """Builds a WKT POLYGON string from a PolygonArea model."""
    # Polygon WKT expects double parentheses: POLYGON((lon lat, lon lat, ...))
    points = ", ".join([f"{lon} {lat}" for lon, lat in polygon.coordinates])
    return f"POLYGON(({points}))"

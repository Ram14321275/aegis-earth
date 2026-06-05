import ee
from datetime import datetime
from app.core.geospatial.models import BoundingBox

def create_bbox_geometry(bbox: BoundingBox) -> ee.Geometry:
    """Converts our domain BoundingBox into a GEE Geometry."""
    return ee.Geometry.BBox(bbox.min_lon, bbox.min_lat, bbox.max_lon, bbox.max_lat)

def apply_date_filter(collection: ee.ImageCollection, start_time: datetime, end_time: datetime) -> ee.ImageCollection:
    """Applies a temporal filter to an ImageCollection."""
    return collection.filterDate(start_time.strftime("%Y-%m-%d"), end_time.strftime("%Y-%m-%d"))

def apply_bounds_filter(collection: ee.ImageCollection, geometry: ee.Geometry) -> ee.ImageCollection:
    """Applies a spatial intersection filter to an ImageCollection."""
    return collection.filterBounds(geometry)

def apply_cloud_cover_filter(collection: ee.ImageCollection, max_cloud_cover: float = 20.0) -> ee.ImageCollection:
    """Applies a cloud cover metadata filter to an ImageCollection (Optical only)."""
    return collection.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud_cover))

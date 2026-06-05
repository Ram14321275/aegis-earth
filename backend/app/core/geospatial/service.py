from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.geospatial.models import BoundingBox, Point, PolygonArea, RadiusSearch
from app.core.geospatial.validators import validate_bounding_box, validate_polygon_closed
from app.db.models.location import Location
from app.db.repositories.geospatial_repository import geospatial_repository

async def get_distance_between_points(session: AsyncSession, p1: Point, p2: Point) -> float:
    """Calculates the distance in meters between two points using PostGIS."""
    return await geospatial_repository.distance_between_points(session, p1.lat, p1.lon, p2.lat, p2.lon)

async def find_locations_within_radius(session: AsyncSession, search: RadiusSearch) -> List[Location]:
    """Finds locations within a specific radius in meters."""
    return await geospatial_repository.within_radius(
        session, 
        lat=search.center.lat, 
        lon=search.center.lon, 
        radius_m=search.radius_meters
    )

async def find_locations_in_bbox(session: AsyncSession, bbox: BoundingBox) -> List[Location]:
    """Finds locations within a bounding box."""
    validate_bounding_box(bbox)
    return await geospatial_repository.within_bbox(
        session,
        min_lon=bbox.min_lon,
        min_lat=bbox.min_lat,
        max_lon=bbox.max_lon,
        max_lat=bbox.max_lat
    )

async def find_locations_in_polygon(session: AsyncSession, polygon: PolygonArea) -> List[Location]:
    """Finds locations that are strictly contained within a polygon."""
    validate_polygon_closed(polygon)
    from app.core.geospatial.calculations import build_polygon_wkt
    wkt = build_polygon_wkt(polygon)
    return await geospatial_repository.within_polygon(session, wkt)

async def find_locations_intersecting_hazard(session: AsyncSession, hazard_polygon: PolygonArea) -> List[Location]:
    """Finds locations that intersect a hazard polygon."""
    validate_polygon_closed(hazard_polygon)
    from app.core.geospatial.calculations import build_polygon_wkt
    wkt = build_polygon_wkt(hazard_polygon)
    return await geospatial_repository.intersects_geometry(session, wkt)

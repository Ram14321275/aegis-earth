import time
from typing import List, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.base_repository import BaseRepository
from app.db.models.location import Location
from app.core.geospatial.calculations import build_point_wkt
from app.core.geospatial.queries import st_dwithin, st_contains, st_intersects, st_distance, st_make_envelope
from app.observability.metrics import metrics_store

class GeospatialRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location)
    
    async def _track_query(self, session: AsyncSession, stmt, operation_name: str) -> Sequence[Location]:
        start_time = time.time()
        try:
            result = await session.execute(stmt)
            locations = result.scalars().all()
            duration_ms = (time.time() - start_time) * 1000
            metrics_store.record_spatial_query(duration_ms, success=True)
            return locations
        except Exception as e:
            metrics_store.record_spatial_query(0.0, success=False)
            raise e

    async def distance_between_points(self, session: AsyncSession, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculates distance between two coordinate pairs natively in the DB."""
        start_time = time.time()
        try:
            from sqlalchemy import select, func
            wkt1 = build_point_wkt(lon1, lat1)
            wkt2 = build_point_wkt(lon2, lat2)
            stmt = select(func.ST_Distance(func.ST_GeogFromText(wkt1), func.ST_GeogFromText(wkt2)))
            result = await session.execute(stmt)
            distance = result.scalar() or 0.0
            duration_ms = (time.time() - start_time) * 1000
            metrics_store.record_spatial_query(duration_ms, success=True)
            return distance
        except Exception as e:
            metrics_store.record_spatial_query(0.0, success=False)
            raise e

    async def within_radius(self, session: AsyncSession, lat: float, lon: float, radius_m: float) -> Sequence[Location]:
        wkt = build_point_wkt(lon, lat)
        stmt = select(Location).where(st_dwithin(Location.point_geometry, wkt, radius_m))
        return await self._track_query(session, stmt, "within_radius")

    async def within_bbox(self, session: AsyncSession, min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> Sequence[Location]:
        # ST_MakeEnvelope creates a Geometry. PostGIS allows geometry-geography intersections, but casting is safer.
        from sqlalchemy import func
        bbox = st_make_envelope(min_lon, min_lat, max_lon, max_lat, 4326)
        stmt = select(Location).where(func.ST_Intersects(Location.point_geometry, bbox))
        return await self._track_query(session, stmt, "within_bbox")

    async def within_polygon(self, session: AsyncSession, polygon_wkt: str) -> Sequence[Location]:
        stmt = select(Location).where(st_contains(Location.point_geometry, polygon_wkt))
        return await self._track_query(session, stmt, "within_polygon")

    async def intersects_geometry(self, session: AsyncSession, wkt: str) -> Sequence[Location]:
        stmt = select(Location).where(st_intersects(Location.point_geometry, wkt))
        return await self._track_query(session, stmt, "intersects_geometry")

geospatial_repository = GeospatialRepository()

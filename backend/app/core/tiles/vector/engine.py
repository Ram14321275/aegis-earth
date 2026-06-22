import logging
from typing import Optional

from sqlalchemy import text
from app.db.session import async_session
from app.core.tiles.optimization.geometry import geometry_optimizer

logger = logging.getLogger(__name__)

class VectorTileEngine:
    """
    Generates Mapbox Vector Tiles (MVT) natively via PostGIS.
    Ensures spatial filtering, dynamic LOD simplification, and tenant isolation.
    """

    @staticmethod
    async def get_hazard_tile(
        tenant_id: str, hazard_type: str, z: int, x: int, y: int
    ) -> Optional[bytes]:
        """
        Retrieves an MVT tile for a specific hazard.
        Uses ST_AsMVT and ST_AsMVTGeom.
        """
        # Calculate bounding box for the tile
        min_lon, min_lat, max_lon, max_lat = geometry_optimizer.tile_to_bbox(x, y, z)
        tolerance = geometry_optimizer.calculate_zoom_tolerance(z)

        # ST_MakeEnvelope uses (xmin, ymin, xmax, ymax) and 4326 is WGS84
        # We transform to 3857 (Web Mercator) for MVT generation
        
        query = text(
            """
            WITH bounds AS (
                SELECT ST_Transform(ST_MakeEnvelope(:min_lon, :min_lat, :max_lon, :max_lat, 4326), 3857) AS geom
            ),
            mvtgeom AS (
                SELECT 
                    ST_AsMVTGeom(
                        ST_Transform(
                            ST_SimplifyPreserveTopology(h.geometry, :tolerance), 
                            3857
                        ), 
                        bounds.geom, 
                        4096, 
                        256, 
                        true
                    ) AS geom,
                    h.id,
                    h.severity,
                    h.confidence
                FROM hazards h, bounds
                WHERE h.hazard_type = :hazard_type
                  AND h.tenant_id = :tenant_id
                  AND ST_Intersects(h.geometry, ST_Transform(bounds.geom, 4326))
            )
            SELECT ST_AsMVT(mvtgeom.*, :layer_name) AS tile
            FROM mvtgeom;
            """
        )

        try:
            async with async_session() as session:
                result = await session.execute(
                    query,
                    {
                        "min_lon": min_lon,
                        "min_lat": min_lat,
                        "max_lon": max_lon,
                        "max_lat": max_lat,
                        "tolerance": tolerance,
                        "hazard_type": hazard_type,
                        "tenant_id": tenant_id,
                        "layer_name": f"{hazard_type}_layer"
                    },
                )
                
                row = result.fetchone()
                if row and row.tile:
                    return bytes(row.tile)
                return None
                
        except Exception as e:
            logger.error(f"Error generating vector tile: {e}")
            return None

vector_tile_engine = VectorTileEngine()

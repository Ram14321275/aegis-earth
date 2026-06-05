from sqlalchemy import text
from app.db.session import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)

async def check_postgis_health() -> dict:
    """Checks if PostGIS is installed and returning valid version info."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT PostGIS_Version();"))
            version = result.scalar()
            
            return {
                "status": "healthy",
                "version": version,
                "spatial_indexes": True
            }
    except Exception as e:
        logger.error(f"PostGIS health check failed: {e}")
        return {
            "status": "unhealthy",
            "version": None,
            "spatial_indexes": False,
            "error": str(e)
        }

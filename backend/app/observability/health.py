from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal
from app.schemas.observability import ComponentHealth, SystemHealthResponse


class HealthAggregator:
    @staticmethod
    async def get_system_health() -> SystemHealthResponse:
        components = {}
        overall_status = "healthy"

        # 1. API Health
        components["api"] = ComponentHealth(status="healthy", details={"version": "v1"})

        # 2. Cache Health
        try:
            from app.core.cache.manager import cache_manager
            cache_status = await cache_manager.get_status()
            components["cache"] = ComponentHealth(
                status=cache_status["status"], 
                details={
                    "type": "redis-backed",
                    "availability": cache_status["availability"],
                    "metrics_summary": cache_status["metrics_summary"]
                }
            )
        except Exception as e:
            components["cache"] = ComponentHealth(
                status="unhealthy", details={"error": str(e)}
            )
            overall_status = "degraded"

        # 3. Database Health
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(text("SELECT 1"))
            components["database"] = ComponentHealth(
                status="healthy", details={"type": "postgresql"}
            )
        except Exception as e:
            components["database"] = ComponentHealth(
                status="unhealthy", details={"error": str(e)}
            )
            overall_status = "degraded"

        # 4. Satellite Provider Health
        try:
            from app.core.satellite.health import get_satellite_system_health
            satellite_health = await get_satellite_system_health()
            if satellite_health["unhealthy"] > 0:
                overall_status = "degraded"
        except Exception as e:
            satellite_health = {"error": str(e)}
            overall_status = "degraded"
            
        # 4.5 GEE Health
        try:
            from app.integrations.gee.health import check_gee_health
            gee_health = await check_gee_health()
            if gee_health["status"] != "healthy":
                overall_status = "degraded"
        except Exception as e:
            gee_health = {"status": "unhealthy", "error": str(e)}
            overall_status = "degraded"
            
        # 4.6 Processing Health
        try:
            from app.core.satellite.service import satellite_service
            from app.core.processing.health import check_processing_health
            from app.core.analysis.flood.health import check_flood_engine_health
            processing_health = check_processing_health()
            flood_health = check_flood_engine_health()
            if processing_health["status"] != "healthy":
                overall_status = "degraded"
            if flood_health["status"] != "healthy":
                overall_status = "degraded"
        except Exception as e:
            processing_health = {"status": "unhealthy", "error": str(e)}
            flood_health = {"status": "unhealthy", "error": str(e)}
            overall_status = "degraded"

        # 5. Alert Engine Health
        try:
            from app.core.alerts.service import alert_service
            alert_status = alert_service.get_status()
            components["alerts"] = ComponentHealth(
                status=alert_status["status"],
                details={"supported_rules": alert_status["supported_rules"]},
            )
        except Exception as e:
            components["alerts"] = ComponentHealth(
                status="unhealthy", details={"error": str(e)}
            )
            overall_status = "degraded"

        # 6. Visualization Engine Health
        try:
            from app.core.visualization.service import visualization_service
            vis_status = visualization_service.get_status()
            components["visualizations"] = ComponentHealth(
                status=vis_status["status"]
            )
        except Exception as e:
            components["visualizations"] = ComponentHealth(
                status="unhealthy", details={"error": str(e)}
            )
            overall_status = "degraded"

        # 7. Database Engine Health
        try:
            from app.db.session import async_session_maker
            from sqlalchemy import text
            async with async_session_maker() as session:
                await session.execute(text("SELECT 1"))
            components["database"] = ComponentHealth(
                status="healthy"
            )
        except Exception as e:
            components["database"] = ComponentHealth(
                status="unhealthy", details={"error": str(e)}
            )
            overall_status = "degraded"

        # 8. Redis Engine Health
        try:
            from app.core.cache.redis_client import redis_client
            import time
            start = time.time()
            ping_ok = await redis_client.ping()
            latency = (time.time() - start) * 1000
            
            if ping_ok:
                components["redis"] = ComponentHealth(
                    status="healthy", details={"latency_ms": f"{latency:.2f}"}
                )
            else:
                components["redis"] = ComponentHealth(
                    status="unhealthy", details={"error": "Ping failed"}
                )
                overall_status = "degraded"
        except Exception as e:
            components["redis"] = ComponentHealth(
                status="unhealthy", details={"error": str(e)}
            )
            overall_status = "degraded"

        from app.observability.metrics import metrics_store
        metrics = metrics_store.get_metrics()
        
        from app.core.jobs.health import get_job_system_health
        jobs_health = await get_job_system_health()
        
        from app.core.workers.health import get_worker_system_health
        workers_health = get_worker_system_health()

        # Wire running jobs count dynamically from busy workers
        jobs_health["running"] = workers_health["busy"]

        from app.core.geospatial.health import check_postgis_health
        postgis_health = await check_postgis_health()
        
        system_status = overall_status
        if processing_health.get("status") != "healthy":
            system_status = "degraded"
        if flood_health.get("status") != "healthy":
            system_status = "degraded"
            
        return SystemHealthResponse(
            status=system_status, 
            components=components,
            jobs=jobs_health,
            workers=workers_health,
            postgis=PostGISHealth(**postgis_health) if postgis_health else None,
            satellite=satellite_health,
            gee=gee_health,
            processing=processing_health,
            flood_engine=flood_health
        )

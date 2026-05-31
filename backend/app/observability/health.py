from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal
from app.providers.contracts import ProviderConfig, ProviderType
from app.providers.manager import ProviderManager
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
                    "type": "in-memory",
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

        # 4. Provider Health
        # We will use ProviderManager until SatelliteFactory is fully implemented
        try:
            settings = get_settings()
            config = ProviderConfig(provider_type=ProviderType(settings.active_provider))
            provider = ProviderManager.get_provider(config)
            
            # Using synchronous health check status logic since it's a mock MVP for now
            components["provider"] = ComponentHealth(
                status="healthy",
                details={"active_provider": settings.active_provider},
            )
        except Exception as e:
            components["provider"] = ComponentHealth(
                status="unhealthy", details={"error": str(e)}
            )
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

        return SystemHealthResponse(
            status=overall_status, components=components
        )

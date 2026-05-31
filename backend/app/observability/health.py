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
        components["cache"] = ComponentHealth(
            status="healthy", details={"type": "in-memory"}
        )

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
        try:
            settings = get_settings()
            provider_type = ProviderType(settings.active_provider)
            config = ProviderConfig(provider_type=provider_type)
            provider = ProviderManager.get_provider(config)

            provider_health = await provider.health_check()
            components["provider"] = ComponentHealth(
                status=provider_health.status.value,
                details={"name": provider.name, "provider_version": provider.version},
            )
            if provider_health.status.value != "healthy":
                overall_status = "degraded"
        except Exception as e:
            components["provider"] = ComponentHealth(
                status="unhealthy", details={"error": str(e)}
            )
            overall_status = "degraded"

        return SystemHealthResponse(status=overall_status, components=components)

from typing import Dict, Any
from app.core.satellite.registry import satellite_registry

async def get_satellite_system_health() -> Dict[str, Any]:
    """
    Polls the registry and evaluates the health of every active provider.
    """
    providers = satellite_registry.list_providers()
    total = len(providers)
    healthy = 0
    unhealthy = 0
    
    details = {}
    
    for provider in providers:
        try:
            status_dict = await provider.health_check()
            if status_dict.get("status") == "healthy":
                healthy += 1
                details[provider.provider_id()] = "healthy"
            else:
                unhealthy += 1
                details[provider.provider_id()] = "unhealthy"
        except Exception as e:
            unhealthy += 1
            details[provider.provider_id()] = f"error: {str(e)}"
            
    return {
        "providers": total,
        "healthy": healthy,
        "unhealthy": unhealthy,
        "details": details
    }

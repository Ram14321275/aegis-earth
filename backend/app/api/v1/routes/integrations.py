from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Dict, Any, List

from app.core.integrations.webhooks.gateway import webhook_gateway
from app.core.integrations.providers.registry import provider_registry
from app.core.integrations.providers.health import provider_health_tracker
from app.core.integrations.humanitarian.coordination import humanitarian_coordinator
from app.core.security.middleware import RBACMiddleware

router = APIRouter(prefix="/integrations", tags=["integrations"])

# Secure Webhook Entrypoint
@router.post("/webhooks/{provider_id}")
async def receive_webhook(provider_id: str, request: Request):
    """
    Receive and securely process incoming webhooks.
    Verifies signatures and routes to ingestion pipeline.
    """
    # In a real scenario, retrieve secret from secure store based on provider_id
    simulated_secret = f"secret_{provider_id}"
    return await webhook_gateway.process_inbound(provider_id, request, simulated_secret)

@router.get("/providers")
async def list_providers():
    """
    List all registered external providers and their health status.
    """
    providers = provider_registry.get_all()
    results = []
    for pid, p in providers.items():
        health = provider_health_tracker.get_status(pid)
        results.append({
            "id": pid,
            "type": p.provider_type,
            "health": health
        })
    return {"providers": results}

@router.post("/humanitarian/request")
async def submit_humanitarian_request(provider_id: str, request_data: Dict[str, Any]):
    """
    Submit a humanitarian coordination request (e.g. NGO shelter mapping).
    """
    return humanitarian_coordinator.process_request(provider_id, request_data)

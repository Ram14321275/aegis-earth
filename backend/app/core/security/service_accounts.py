from datetime import timedelta
from app.core.security.jwt import create_token
from app.core.security.permissions import SystemPermission

def generate_worker_token(worker_id: str, tenant_id: str) -> str:
    """
    Generates an internal service token for background workers.
    """
    expires_delta = timedelta(hours=24) # Scoped duration
    # Workers usually get automation-agent roles
    return create_token(
        subject=f"worker:{worker_id}",
        tenant_id=tenant_id,
        role="automation-agent",
        expires_delta=expires_delta,
        token_type="service"
    )

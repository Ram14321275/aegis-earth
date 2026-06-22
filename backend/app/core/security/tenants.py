import contextvars
from typing import Optional

# Context variables for tenant and user state
current_tenant_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "current_tenant_id", default=None
)

current_user: contextvars.ContextVar[Optional[dict]] = contextvars.ContextVar(
    "current_user", default=None
)

def get_current_tenant_id() -> Optional[str]:
    """Retrieve the current tenant ID from context."""
    return current_tenant_id.get()

def set_current_tenant_id(tenant_id: Optional[str]) -> contextvars.Token:
    """Set the current tenant ID in context."""
    return current_tenant_id.set(tenant_id)

def get_current_user() -> Optional[dict]:
    """Retrieve the current user payload from context."""
    return current_user.get()

def set_current_user(user: Optional[dict]) -> contextvars.Token:
    """Set the current user payload in context."""
    return current_user.set(user)

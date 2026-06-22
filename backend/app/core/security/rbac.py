from typing import Set
from .permissions import SystemPermission

# Policy-driven RBAC mapping
ROLE_POLICIES = {
    "admin": {
        p.value for p in SystemPermission
    },
    "analyst": {
        SystemPermission.READ_INTELLIGENCE.value,
        SystemPermission.WRITE_INTELLIGENCE.value,
        SystemPermission.SUBSCRIBE_ALERTS.value,
        SystemPermission.SUBSCRIBE_EVENTS.value,
    },
    "viewer": {
        SystemPermission.READ_INTELLIGENCE.value,
        SystemPermission.SUBSCRIBE_ALERTS.value,
    },
    "operator": {
        SystemPermission.READ_INTELLIGENCE.value,
        SystemPermission.SUBSCRIBE_ALERTS.value,
        SystemPermission.SUBSCRIBE_EVENTS.value,
        SystemPermission.EXECUTE_JOBS.value,
    },
    "automation-agent": {
        SystemPermission.READ_INTELLIGENCE.value,
        SystemPermission.WRITE_INTELLIGENCE.value,
        SystemPermission.EXECUTE_JOBS.value,
        SystemPermission.UPDATE_RISK.value,
        SystemPermission.SUBSCRIBE_EVENTS.value,
    }
}

def get_role_permissions(role: str) -> Set[str]:
    """Returns the set of permissions for a given role."""
    return ROLE_POLICIES.get(role, set())

def has_permission(user_role: str, required_permission: str) -> bool:
    """Checks if a role has a specific permission."""
    perms = get_role_permissions(user_role)
    return required_permission in perms

import pytest
from app.core.security.rbac import has_permission
from app.core.security.permissions import SystemPermission

def test_admin_has_all_permissions():
    assert has_permission("admin", SystemPermission.MANAGE_TENANT.value)
    assert has_permission("admin", SystemPermission.READ_INTELLIGENCE.value)

def test_viewer_permissions():
    assert has_permission("viewer", SystemPermission.READ_INTELLIGENCE.value)
    assert not has_permission("viewer", SystemPermission.WRITE_INTELLIGENCE.value)
    assert not has_permission("viewer", SystemPermission.MANAGE_TENANT.value)

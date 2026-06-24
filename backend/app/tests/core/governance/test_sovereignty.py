import pytest
from app.core.governance.sovereignty.middleware import SovereigntyBoundaryResolver

def test_sovereignty_isolation():
    resolver = SovereigntyBoundaryResolver()
    
    # Allowed
    assert resolver.is_export_allowed("tenant_iso_strict", "US") is True
    assert resolver.is_export_allowed("tenant_iso_strict", "CA") is True
    
    # Blocked
    assert resolver.is_export_allowed("tenant_iso_strict", "EU") is False
    assert resolver.is_export_allowed("tenant_eu_only", "US") is False
    
    # Unrestricted tenant
    assert resolver.is_export_allowed("tenant_unrestricted", "US") is True
    assert resolver.is_export_allowed("tenant_unrestricted", "CN") is True

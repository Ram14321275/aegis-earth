import pytest
from app.core.edge.sovereignty.partitioning import partition_manager
from app.core.edge.routing.sovereign_router import sovereign_router
from app.core.edge.topology.registry import edge_registry
from app.core.edge.topology.models import EdgeNodeConfig

def test_sovereign_routing():
    # Setup topology
    edge_registry._nodes = {}
    edge_registry._configs = {}
    
    edge_registry.register_node(EdgeNodeConfig(node_id="node_us", sovereign_region="US-EAST", jurisdiction="US"))
    edge_registry.register_node(EdgeNodeConfig(node_id="node_eu", sovereign_region="EU-CENTRAL", jurisdiction="EU"))
    
    # Test routing for restricted tenant
    targets_us_gov = sovereign_router.route_request("tenant_us_gov", {"data": "test"})
    assert "node_us" in targets_us_gov
    assert "node_eu" not in targets_us_gov
    
    # Test routing for unrestricted tenant
    targets_unrestricted = sovereign_router.route_request("tenant_global", {"data": "test"})
    assert "node_us" in targets_unrestricted
    assert "node_eu" in targets_unrestricted

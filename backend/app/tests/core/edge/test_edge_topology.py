import pytest
from app.core.edge.topology.registry import edge_registry
from app.core.edge.topology.models import EdgeNodeConfig

def test_edge_topology_registry():
    config = EdgeNodeConfig(node_id="node_topo_1", sovereign_region="US-WEST", jurisdiction="US")
    
    # Register
    state = edge_registry.register_node(config)
    assert state.node_id == "node_topo_1"
    assert state.health_state == "ACTIVE"
    
    # Heartbeat
    edge_registry.update_heartbeat("node_topo_1", "DEGRADED")
    updated_state = edge_registry.get_node_state("node_topo_1")
    assert updated_state.health_state == "DEGRADED"

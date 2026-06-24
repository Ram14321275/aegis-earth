import pytest
from app.core.resilience.mesh.topology import resilience_mesh

def test_mesh_health_calculation():
    assert resilience_mesh.calculate_mesh_health() == 100.0
    
    resilience_mesh.register_node("node_1", "US-EAST", 100)
    resilience_mesh.register_node("node_2", "US-WEST", 100)
    
    # Degrade node 2
    resilience_mesh.nodes["node_2"]["survivability_score"] = 50.0
    
    assert resilience_mesh.calculate_mesh_health() == 75.0

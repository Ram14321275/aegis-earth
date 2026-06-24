import pytest
from app.core.economics.allocation.engine import resource_allocation_engine

def test_resource_allocation():
    requests = [
        {"target_region": "R1", "requested_amount": 100, "criticality": 3.0},
        {"target_region": "R2", "requested_amount": 100, "criticality": 1.0}
    ]
    res = resource_allocation_engine.allocate_resources("medical", 100.0, requests)
    
    assert res["total_allocated"] <= 100.0
    # R1 has weight 3/4, gets 75. R2 has weight 1/4, gets 25.
    allocs = {a["target_region"]: a["amount"] for a in res["allocations"]}
    assert allocs["R1"] == 75.0
    assert allocs["R2"] == 25.0
    assert "reasoning_hash" in res

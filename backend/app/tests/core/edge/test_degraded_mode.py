import pytest
from app.core.edge.degraded.engine import degraded_engine
from app.core.edge.offline.queue import offline_queue

def test_degraded_mode_engine():
    offline_queue._queues = {}
    
    degraded_engine.activate_degraded_mode("node_deg_1")
    degraded_engine.handle_degraded_operation("node_deg_1", {"type": "HAZARD_DETECTED"})
    
    q = offline_queue.get_queued_events("node_deg_1")
    assert len(q) == 1
    assert q[0]["type"] == "HAZARD_DETECTED"
    assert "offline_timestamp" in q[0]

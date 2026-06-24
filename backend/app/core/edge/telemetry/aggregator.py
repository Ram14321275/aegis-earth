from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class TelemetryAggregator:
    """Aggregates edge metrics before syncing to avoid chatty networks."""
    def __init__(self):
        self._buffers: Dict[str, List[Dict[str, Any]]] = {}

    def buffer_telemetry(self, node_id: str, telemetry: Dict[str, Any]):
        if node_id not in self._buffers:
            self._buffers[node_id] = []
        self._buffers[node_id].append(telemetry)

    def flush_telemetry(self, node_id: str) -> List[Dict[str, Any]]:
        return self._buffers.pop(node_id, [])

telemetry_aggregator = TelemetryAggregator()

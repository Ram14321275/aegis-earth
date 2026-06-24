from typing import Dict, List, Optional
from datetime import datetime, timezone
import logging

from app.core.edge.topology.models import EdgeNodeConfig, EdgeNodeState
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class EdgeNodeRegistry:
    def __init__(self):
        # MVP: Simulating database state in-memory since migrations are deferred.
        self._nodes: Dict[str, EdgeNodeState] = {}
        self._configs: Dict[str, EdgeNodeConfig] = {}

    def register_node(self, config: EdgeNodeConfig) -> EdgeNodeState:
        """Registers a new edge node in the topology graph."""
        self._configs[config.node_id] = config
        
        state = EdgeNodeState(
            node_id=config.node_id,
            health_state="ACTIVE",
            synchronization_state="IN_SYNC",
            last_heartbeat=datetime.now(timezone.utc)
        )
        self._nodes[config.node_id] = state
        
        metrics_store.record_integrations_action("edge_nodes_total") # Mapped to integration/edge metrics conceptually, we'll update metrics later
        logger.info(f"Registered Edge Node {config.node_id} in region {config.sovereign_region}")
        return state

    def update_heartbeat(self, node_id: str, health_state: str) -> None:
        """Updates the heartbeat and health state of a node."""
        if node_id in self._nodes:
            self._nodes[node_id].last_heartbeat = datetime.now(timezone.utc)
            self._nodes[node_id].health_state = health_state
            logger.debug(f"Heartbeat updated for Edge Node {node_id}: {health_state}")

    def get_active_nodes_in_region(self, region: str) -> List[EdgeNodeState]:
        """Returns active nodes for sovereign shard routing."""
        active_nodes = []
        for node_id, state in self._nodes.items():
            if state.health_state == "ACTIVE":
                config = self._configs.get(node_id)
                if config and config.sovereign_region == region:
                    active_nodes.append(state)
        return active_nodes

    def get_node_state(self, node_id: str) -> Optional[EdgeNodeState]:
        return self._nodes.get(node_id)

edge_registry = EdgeNodeRegistry()

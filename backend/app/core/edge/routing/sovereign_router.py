from typing import Dict, Any, Optional, List
import logging

from app.core.edge.sovereignty.partitioning import partition_manager
from app.core.edge.topology.registry import edge_registry

logger = logging.getLogger(__name__)

class SovereignRouter:
    """Dispatches requests exclusively to explicitly permitted sovereign shards."""
    
    def route_request(self, tenant_id: str, payload: Dict[str, Any]) -> List[str]:
        """
        Determines the edge node IDs that are legally permitted to receive this payload.
        """
        allowed_nodes = []
        # Get all registered nodes (in a real system we'd use a graph query)
        for node_id, state in edge_registry._nodes.items():
            if state.health_state != "ACTIVE":
                continue
                
            config = edge_registry._configs.get(node_id)
            if not config:
                continue
                
            if partition_manager.is_region_allowed(tenant_id, config.sovereign_region):
                allowed_nodes.append(node_id)
        
        if not allowed_nodes:
            logger.warning(f"No sovereign routing targets available for tenant {tenant_id}")
            
        return allowed_nodes

sovereign_router = SovereignRouter()

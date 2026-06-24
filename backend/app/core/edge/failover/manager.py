import logging
from typing import Optional

from app.core.edge.elections.leader import leader_election
from app.observability.metrics import metrics_store
from app.core.edge.degraded.engine import degraded_engine

logger = logging.getLogger(__name__)

class FailoverManager:
    """Manages regional failovers and split-brain prevention."""
    
    async def handle_node_failure(self, failed_node_id: str, region: str, fallback_node_id: str):
        """
        Orchestrates failover. Will attempt to promote fallback_node_id.
        """
        metrics_store.record_edge_action("failover_events_total")
        logger.warning(f"Initiating failover for region {region} from {failed_node_id} to {fallback_node_id}")
        
        # Force release of failed node if possible (in reality, let Redis TTL expire)
        # We attempt to acquire leadership for the fallback
        success, token = await leader_election.acquire_leadership(region, fallback_node_id)
        
        if success:
            logger.info(f"Failover successful. Node {fallback_node_id} is now leader of {region}.")
        else:
            logger.error(f"Failover failed. Node {fallback_node_id} could not acquire leadership. Split-brain prevented.")
            metrics_store.record_edge_action("split_brain_preventions_total")
            
            # Activate degraded mode for the fallback node since it can't lead but might still receive local traffic
            degraded_engine.activate_degraded_mode(fallback_node_id)

failover_manager = FailoverManager()

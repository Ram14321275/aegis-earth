from typing import Dict, Any, List
import logging
from datetime import datetime, timezone

from app.core.edge.consistency.verifier import consistency_verifier
from app.core.edge.offline.queue import offline_queue
from app.core.edge.synchronization.orchestrator import sync_orchestrator
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class RecoveryEngine:
    """Orchestrates edge node restoration and offline queue flushing."""
    
    async def initiate_recovery(self, node_id: str) -> bool:
        """Attempts to catch up a disconnected node."""
        start_time = datetime.now()
        metrics_store.record_edge_action("recovery_sessions_total")
        logger.info(f"Initiating recovery session for node {node_id}")
        
        # 1. Flush offline queue
        queued_events = offline_queue.get_queued_events(node_id)
        if queued_events:
            logger.info(f"Flushing {len(queued_events)} offline events for {node_id}")
            
            # 2. Validate local lineage before pushing
            if not consistency_verifier.verify_lineage(queued_events):
                logger.error(f"Recovery aborted for {node_id}: corrupted offline lineage.")
                return False
                
            # 3. Synchronize with orchestrator
            success = await sync_orchestrator.process_sync_batch(node_id, queued_events)
            if not success:
                logger.error(f"Recovery sync failed for {node_id}")
                return False
                
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        metrics_store.record_edge_action("recovery_duration_ms", duration_ms) # Example if we support values, else just track total
        logger.info(f"Recovery successful for {node_id}")
        return True

recovery_engine = RecoveryEngine()

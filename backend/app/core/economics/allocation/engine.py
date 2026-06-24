from typing import Dict, Any, List
import logging
import uuid
import hashlib

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class ResourceAllocationEngine:
    """Deterministic, weighted resource allocation balancing scarcity and infrastructure priority."""
    
    def allocate_resources(self, resource_type: str, total_available: float, requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Allocates resources deterministically based on node criticality."""
        
        # Normalize criticalities
        total_criticality = sum(r.get("criticality", 1.0) for r in requests)
        
        allocations = []
        distributed_total = 0.0
        
        for req in sorted(requests, key=lambda x: x.get("criticality", 1.0), reverse=True):
            criticality = req.get("criticality", 1.0)
            target = req.get("target_region")
            requested_amount = req.get("requested_amount", 0.0)
            
            # Weighted slice
            weight = criticality / total_criticality if total_criticality > 0 else 0
            fair_share = total_available * weight
            
            granted = min(requested_amount, fair_share)
            
            allocations.append({
                "target_region": target,
                "amount": granted
            })
            distributed_total += granted
            
        reasoning = f"avail:{total_available}|reqs:{len(requests)}|dist:{distributed_total}"
        reasoning_hash = hashlib.sha256(reasoning.encode()).hexdigest()
        
        return {
            "allocation_id": f"alloc-{uuid.uuid4()}",
            "resource_type": resource_type,
            "total_allocated": distributed_total,
            "allocations": allocations,
            "reasoning_hash": reasoning_hash,
            "rollback_strategy": {"method": "revoke_allocations"}
        }

resource_allocation_engine = ResourceAllocationEngine()

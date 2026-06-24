from typing import Dict, Any, List
import logging
import uuid
import hashlib

from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class EconomicDisruptionEngine:
    """Calculates cascading disruption depths and impact scores."""
    
    def calculate_disruption(self, root_cause_severity: float, dependencies: int) -> Dict[str, Any]:
        """Deterministically evaluates disruption scale based on dependencies."""
        
        # Simple deterministic formula
        impact_score = min(1.0, root_cause_severity * (1 + (0.1 * dependencies)))
        cascading_depth = dependencies if root_cause_severity > 0.5 else int(dependencies / 2)
        
        reasoning = f"sev:{root_cause_severity}|deps:{dependencies}=>{impact_score}"
        reasoning_hash = hashlib.sha256(reasoning.encode()).hexdigest()
        
        if cascading_depth > 0:
            metrics_store.record_economic_action("disruption_propagation_depth", float(cascading_depth))
            
        return {
            "disruption_id": f"dis-{uuid.uuid4()}",
            "impact_score": impact_score,
            "cascading_depth": cascading_depth,
            "reasoning_hash": reasoning_hash,
            "lineage_reference": "lin-root" # Hooked into lineage system later
        }

economic_disruption_engine = EconomicDisruptionEngine()

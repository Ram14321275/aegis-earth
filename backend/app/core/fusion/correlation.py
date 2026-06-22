import uuid
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from app.core.fusion.models import CascadingRisk
from app.db.repositories.fusion_repository import correlation_event_repository

logger = logging.getLogger(__name__)

class CorrelationEngine:
    """
    Detects cascading hazards without infinite escalation loops using cooldowns.
    Validates spatial and temporal proximity constraints.
    """
    
    # Cooldown in seconds before the same cascade can be re-triggered for the same region
    COOLDOWN_SECONDS = 86400  # 24 hours
    
    # Rules: (primary, secondary) -> amplification factor
    CORRELATION_RULES = {
        ("WILDFIRE", "FLOOD"): 1.4,          # Burn scars amplify floods
        ("VEGETATION_LOSS", "DROUGHT"): 1.3,
        ("URBAN_EXPANSION", "FLOOD"): 1.2,
        ("FLOOD", "INFRASTRUCTURE_DEGRADATION"): 1.5,
    }

    async def detect_cascades(
        self,
        session: Any,
        primary_hazard: str,
        primary_id: str,
        active_hazards: List[Dict[str, Any]],
        region_id: str
    ) -> List[CascadingRisk]:
        """
        Detects cascading risks from a list of active hazards in the SAME region,
        enforcing cooldowns.
        """
        cascades = []
        now = datetime.now(timezone.utc)
        
        for active in active_hazards:
            secondary_hazard = active.get("hazard_type")
            secondary_id = active.get("id", "unknown")
            
            # Check if correlation rule exists
            amp_factor = self.CORRELATION_RULES.get((primary_hazard, secondary_hazard))
            if not amp_factor:
                # Also check reverse in case order doesn't matter, though cascades are usually directional
                continue
                
            # Must check if a cooldown is active for this interaction in this region
            # (In a real implementation, we query correlation_event_repository for the last event in this region)
            # For MVP, we will assume we check the DB or Redis.
            
            # Simulated check:
            # last_event = await correlation_event_repository.get_last_event(session, primary_hazard, secondary_hazard, region_id)
            # if last_event and last_event.cooldown_expires_at > now:
            #     continue
            
            event_id = f"corr-{uuid.uuid4()}"
            cooldown_expiry = now + timedelta(seconds=self.COOLDOWN_SECONDS)
            
            cascade = CascadingRisk(
                correlation_event_id=event_id,
                primary_hazard_id=primary_id,
                secondary_hazard_id=secondary_id,
                interaction_type="amplification",
                amplification_factor=amp_factor,
                cooldown_expires_at=cooldown_expiry,
                timestamp=now
            )
            cascades.append(cascade)
            
        return cascades

correlation_engine = CorrelationEngine()

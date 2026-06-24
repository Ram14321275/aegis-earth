from typing import List, Dict, Any
import logging
from app.core.governance.interfaces import SovereigntyResolver
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class SovereigntyBoundaryResolver(SovereigntyResolver):
    def __init__(self):
        # MVP: hardcoded mock rules. In production, load from DB.
        self.tenant_restrictions = {
            "tenant_iso_strict": ["US", "CA"], # Only allowed to export to US, CA
            "tenant_eu_only": ["EU"]
        }

    def is_export_allowed(self, tenant_id: str, target_region: str) -> bool:
        """
        Validates if a cross-border export or integration is legally permitted.
        """
        allowed_regions = self.tenant_restrictions.get(tenant_id)
        if allowed_regions is None:
            return True # Unrestricted tenant
            
        if target_region not in allowed_regions:
            metrics_store.record_governance_action("sovereignty_blocked_operations_total")
            logger.warning(f"Sovereignty Blocked: Tenant {tenant_id} attempted export to {target_region}")
            return False
            
        return True

sovereignty_resolver = SovereigntyBoundaryResolver()

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SovereignPartitionManager:
    """Manages explicit geopolitical intelligence partitions."""
    
    def __init__(self):
        # Mock configuration. e.g. tenant -> valid edge regions
        self.tenant_partitions = {
            "tenant_us_gov": ["US-EAST", "US-WEST"],
            "tenant_eu_local": ["EU-CENTRAL"]
        }

    def get_allowed_partitions(self, tenant_id: str) -> list[str]:
        return self.tenant_partitions.get(tenant_id, [])

    def is_region_allowed(self, tenant_id: str, target_region: str) -> bool:
        """Determines if a tenant is allowed to synchronize to a specific edge region."""
        allowed = self.get_allowed_partitions(tenant_id)
        if not allowed:
            return True # Unrestricted
        return target_region in allowed

partition_manager = SovereignPartitionManager()

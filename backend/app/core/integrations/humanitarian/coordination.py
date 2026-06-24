import logging
from typing import Dict, Any, List
from datetime import datetime, timezone
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class HumanitarianCoordinator:
    def process_request(self, provider_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a humanitarian request (e.g., NGO resource request, shelter mapping).
        All prioritization must remain deterministic and explainable.
        """
        metrics_store.record_command_center_action("humanitarian_requests_total")
        
        request_type = request_data.get("type", "unknown")
        
        try:
            priority = self._calculate_deterministic_priority(request_data)
            
            # Simulated storage
            response = {
                "request_id": f"hum-{int(datetime.now(timezone.utc).timestamp())}",
                "provider_id": provider_id,
                "request_type": request_type,
                "priority": priority,
                "status": "acknowledged",
                "explainability": f"Priority '{priority}' assigned based on deterministic rules."
            }
            logger.info(f"Processed humanitarian request {response['request_id']} with priority {priority}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to process humanitarian request from {provider_id}: {e}")
            raise

    def _calculate_deterministic_priority(self, data: Dict[str, Any]) -> str:
        """
        Deterministic prioritization. No black-box AI.
        """
        severity_flags = data.get("severity_flags", [])
        impact_count = data.get("impacted_population", 0)
        
        if "immediate_life_threat" in severity_flags or impact_count > 10000:
            return "CRITICAL"
        elif "resource_depletion" in severity_flags or impact_count > 1000:
            return "HIGH"
        else:
            return "NORMAL"

humanitarian_coordinator = HumanitarianCoordinator()

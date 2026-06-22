from datetime import datetime
from typing import Any, Dict, Optional
from app.core.jobs.interfaces import SchedulerInterface
from app.core.jobs.queue import redis_queue

class PriorityScheduler(SchedulerInterface):
    async def schedule(self, payload: Dict[str, Any], scheduled_at: Optional[datetime] = None) -> None:
        """
        Calculates priority and pushes to the corresponding queue.
        """
        priority_score = self._calculate_priority(payload)
        payload["computed_priority"] = priority_score

        # Queue routing based on priority score
        if priority_score >= 80:
            queue_name = "high"
        elif priority_score >= 40:
            queue_name = "default"
        else:
            queue_name = "low"
        
        await redis_queue.enqueue(queue_name, payload, priority=priority_score)

    def _calculate_priority(self, payload: Dict[str, Any]) -> float:
        """
        Priority scoring combining severity, risk, SLA, population density.
        Max score 100.
        """
        score = 0.0
        
        metadata = payload.get("metadata_data", {}) or {}
        
        # 1. Disaster Severity (0-40)
        severity = metadata.get("severity", "LOW").upper()
        if severity == "CRITICAL":
            score += 40
        elif severity == "HIGH":
            score += 30
        elif severity == "MEDIUM":
            score += 15
        
        # 2. Human Risk / Population Density (0-30)
        population_density = metadata.get("population_density", 0)
        if population_density > 10000:
            score += 30
        elif population_density > 1000:
            score += 20
        elif population_density > 100:
            score += 10

        # 3. Tenant SLA (0-20)
        sla_tier = metadata.get("tenant_tier", "standard").lower()
        if sla_tier == "enterprise":
            score += 20
        elif sla_tier == "premium":
            score += 10
            
        # 4. Request Urgency (0-10)
        is_urgent = metadata.get("is_urgent", False)
        if is_urgent:
            score += 10
            
        return min(score, 100.0)

job_scheduler = PriorityScheduler()

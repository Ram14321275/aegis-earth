import uuid
import time
import logging
from typing import List

from app.core.copilot.models import (
    CopilotResponse, MissionContext, ThreatSummary, OperationalInsight,
    CopilotReasoningTrace, CopilotDegradationMode
)
from app.core.copilot.narratives.engine import DeterministicNarrativeEngine
from app.core.copilot.recommendations.engine import DeterministicRecommendationEngine
from app.core.copilot.governance.policy import GovernanceEngine
from app.core.copilot.explainability.validator import ExplainabilityValidator
from app.core.copilot.memory.manager import MissionMemoryManager
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)


class CopilotOrchestrator:
    """
    Central orchestrator for the AI Copilot layer.
    Coordinates deterministic narrative generation, recommendations, governance, and explainability validation.
    """

    def __init__(self):
        self.narrative_engine = DeterministicNarrativeEngine()
        self.recommendation_engine = DeterministicRecommendationEngine()
        self.governance_engine = GovernanceEngine()
        self.explainability_validator = ExplainabilityValidator()
        self.memory_manager = MissionMemoryManager()

    async def generate_mission_intelligence(
        self,
        tenant_id: str,
        mission_id: str,
        context: MissionContext,
        threats: List[ThreatSummary],
        insights: List[OperationalInsight],
        degradation_mode: CopilotDegradationMode = CopilotDegradationMode.FULL_INTELLIGENCE,
        degraded_reason: str = None
    ) -> CopilotResponse:
        start_time = time.time()
        
        # 1. Base Trace
        trace = CopilotReasoningTrace(
            trace_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            source_systems=["fusion_engine", "predictive_engine"] if degradation_mode == CopilotDegradationMode.FULL_INTELLIGENCE else ["fusion_engine"],
            reasoning_hash="",
            evidence_hash=str(hash(str([t.model_dump() for t in threats]) + str([i.model_dump() for i in insights]))),
            degradation_mode=degradation_mode,
            degraded_reason=degraded_reason
        )

        # 2. Generate Narrative
        try:
            narrative = self.narrative_engine.generate_detailed_report(context, threats, insights, trace)
        except Exception as e:
            logger.error(f"Narrative generation failed: {e}")
            metrics_store.record_command_center_action("explainability_fallback_total")
            trace.degradation_mode = CopilotDegradationMode.SAFE_FALLBACK
            trace.degraded_reason = "Narrative engine exception"
            narrative = self.narrative_engine.generate_short_summary(context, threats, trace)

        # 3. Generate Recommendations
        try:
            raw_recs = self.recommendation_engine.generate_recommendations(threats)
            
            # 4. Apply Governance
            safe_recs = []
            for rec in raw_recs:
                gov_rec = self.governance_engine.evaluate(rec)
                safe_recs.append(gov_rec)
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            metrics_store.record_command_center_action("copilot_degraded_responses_total")
            safe_recs = []

        # 5. Assemble Response
        response = CopilotResponse(
            response_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            mission_id=mission_id,
            narrative=narrative,
            recommendations=safe_recs,
            insights=insights,
            threats=threats,
            trace=trace
        )

        # 6. Explainability Validation
        is_valid, violations = self.explainability_validator.validate(response)
        if not is_valid:
            logger.warning(f"Explainability validation failed for CopilotResponse {response.response_id}")
            metrics_store.record_command_center_action("copilot_degraded_responses_total")

        duration = (time.time() - start_time) * 1000
        metrics_store.record_command_center_action("mission_context_assembly_duration_ms", duration)
        
        return response

import uuid
from typing import List

from app.core.copilot.models import (
    ThreatSummary, CopilotRecommendation, ConfidenceAssessment, 
    ConfidenceLevel, RecommendationImpact, RecommendationRollback
)
from app.core.copilot.interfaces.recommendation import RecommendationEngineInterface
from app.observability.metrics import metrics_store


class DeterministicRecommendationEngine(RecommendationEngineInterface):
    """
    Deterministic template-driven recommendation engine.
    Ensures safe, explainable actions based on threat vectors.
    """

    def generate_recommendations(self, threats: List[ThreatSummary]) -> List[CopilotRecommendation]:
        recommendations = []
        for threat in threats:
            if threat.severity == "CRITICAL":
                recommendations.append(self._build_escalation(threat))
            elif threat.severity == "HIGH":
                recommendations.append(self._build_increase_monitoring(threat))
            elif threat.severity in ["MODERATE", "LOW"]:
                recommendations.append(self._build_standard_monitoring(threat))
                
        metrics_store.record_command_center_action("recommendation_generation_total", len(recommendations))
        return recommendations

    def _build_escalation(self, threat: ThreatSummary) -> CopilotRecommendation:
        return CopilotRecommendation(
            id=str(uuid.uuid4()),
            action_type="escalate_human_review",
            title=f"Escalate {threat.hazard_type} for Human Review",
            rationale=f"Critical {threat.hazard_type} detected in {threat.affected_area}. Requires immediate human validation.",
            evidence_chain=[f"Threat severity is CRITICAL for {threat.hazard_type}", f"Impact: {threat.estimated_impact}"],
            operational_severity="CRITICAL",
            confidence=ConfidenceAssessment(
                score=0.95, level=ConfidenceLevel.CRITICAL, 
                explanation="Deterministic critical threat mapping"
            ),
            impact=RecommendationImpact(
                resource_cost="HIGH", time_to_implement="IMMEDIATE", 
                expected_outcome="Human awareness and potential action"
            ),
            rollback=RecommendationRollback(
                strategy="Stand down alert", time_to_rollback="MINUTES", complexity="LOW"
            )
        )

    def _build_increase_monitoring(self, threat: ThreatSummary) -> CopilotRecommendation:
        return CopilotRecommendation(
            id=str(uuid.uuid4()),
            action_type="increase_monitoring",
            title=f"Increase Monitoring for {threat.hazard_type}",
            rationale=f"High {threat.hazard_type} detected. Proactive monitoring recommended.",
            evidence_chain=[f"Threat severity is HIGH for {threat.hazard_type}"],
            operational_severity="HIGH",
            confidence=ConfidenceAssessment(
                score=0.85, level=ConfidenceLevel.HIGH, 
                explanation="Deterministic high threat mapping"
            ),
            impact=RecommendationImpact(
                resource_cost="MEDIUM", time_to_implement="HOURS", 
                expected_outcome="Enhanced situational awareness"
            ),
            rollback=RecommendationRollback(
                strategy="Revert to standard monitoring", time_to_rollback="MINUTES", complexity="LOW"
            )
        )

    def _build_standard_monitoring(self, threat: ThreatSummary) -> CopilotRecommendation:
        return CopilotRecommendation(
            id=str(uuid.uuid4()),
            action_type="maintain_monitoring",
            title=f"Maintain Monitoring for {threat.hazard_type}",
            rationale=f"{threat.severity} {threat.hazard_type} detected. Routine monitoring applies.",
            evidence_chain=[f"Threat severity is {threat.severity}"],
            operational_severity=threat.severity,
            confidence=ConfidenceAssessment(
                score=0.60, level=ConfidenceLevel.MODERATE, 
                explanation="Deterministic moderate/low threat mapping"
            ),
            impact=RecommendationImpact(
                resource_cost="LOW", time_to_implement="IMMEDIATE", 
                expected_outcome="Standard operational posture"
            ),
            rollback=RecommendationRollback(
                strategy="None", time_to_rollback="NONE", complexity="NONE"
            )
        )

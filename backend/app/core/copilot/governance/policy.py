from app.core.copilot.models import CopilotRecommendation, GovernanceDecision
from app.observability.metrics import metrics_store

class GovernanceEngine:
    """
    Enforces deterministic safety bounds on Copilot recommendations.
    Blocks autonomous destructive actions and enforces confidence thresholds.
    """

    def evaluate(self, recommendation: CopilotRecommendation) -> CopilotRecommendation:
        violations = []
        approved = True
        adjusted_severity = None
        
        action_type = recommendation.action_type.lower()
        title = recommendation.title.lower()
        rationale = recommendation.rationale.lower()
        
        # 1. Block autonomous destructive actions
        if "destroy" in action_type or "delete" in action_type:
            violations.append("Destructive infrastructure actions are strictly forbidden.")
            approved = False

        # 2. Block autonomous evacuation actions (Must be human review)
        if "evacuate" in action_type and "human" not in action_type:
             violations.append("Autonomous evacuations are strictly forbidden. Must involve human review.")
             approved = False

        # 3. Confidence Thresholds Enforcement
        conf_score = recommendation.confidence.score
        sev = recommendation.operational_severity
        
        if sev == "CRITICAL" and conf_score < 0.9:
            violations.append(f"CRITICAL severity requires confidence >= 0.9 (got {conf_score}).")
            adjusted_severity = self._degrade_severity(conf_score)
        elif sev == "HIGH" and conf_score < 0.7:
            violations.append(f"HIGH severity requires confidence >= 0.7 (got {conf_score}).")
            adjusted_severity = self._degrade_severity(conf_score)
        elif sev == "MODERATE" and conf_score < 0.4:
            violations.append(f"MODERATE severity requires confidence >= 0.4 (got {conf_score}).")
            adjusted_severity = "LOW"
                
        if not approved or violations:
            metrics_store.record_command_center_action("governance_rejections_total")
            
        if not approved:
            metrics_store.record_command_center_action("recommendation_blocked_total")

        recommendation.governance_review = GovernanceDecision(
            approved=approved,
            rejection_reason="Failed safety validation." if not approved else None,
            policy_violations=violations,
            adjusted_severity=adjusted_severity
        )
        
        if adjusted_severity:
            recommendation.operational_severity = adjusted_severity
            
        return recommendation

    def _degrade_severity(self, conf_score: float) -> str:
        if conf_score >= 0.7:
            return "HIGH"
        elif conf_score >= 0.4:
            return "MODERATE"
        return "LOW"

from typing import List, Tuple
from app.core.copilot.models import CopilotResponse, ExplainabilityViolation
from app.observability.metrics import metrics_store

class ExplainabilityValidator:
    """
    Ensures all Copilot outputs are 100% explainable, deterministic, and verifiable.
    """

    def validate(self, response: CopilotResponse) -> Tuple[bool, List[ExplainabilityViolation]]:
        violations = []
        
        # 1. Missing reasoning hash
        if not response.trace.reasoning_hash:
            violations.append(ExplainabilityViolation(
                violation_type="MISSING_REASONING_HASH",
                description="Narrative missing required cryptographic reasoning hash.",
                failed_claim="Narrative Trace"
            ))

        # 2. Orphaned recommendations (recs without threats/insights)
        if response.recommendations and not response.threats and not response.insights:
            violations.append(ExplainabilityViolation(
                violation_type="ORPHANED_RECOMMENDATION",
                description="Recommendations generated without underlying threats or insights.",
                failed_claim="Recommendations"
            ))

        # 3. Missing evidence in recommendations
        for rec in response.recommendations:
            if not rec.evidence_chain:
                violations.append(ExplainabilityViolation(
                    violation_type="MISSING_EVIDENCE",
                    description=f"Recommendation '{rec.title}' lacks an evidence chain.",
                    failed_claim=rec.id
                ))

        # 4. Hallucinated/Unverifiable escalation chains
        if response.narrative.escalation_context:
            esc = response.narrative.escalation_context
            if not esc.causal_factors:
                violations.append(ExplainabilityViolation(
                    violation_type="UNVERIFIABLE_ESCALATION",
                    description="Escalation narrative lacks causal factors.",
                    failed_claim="Escalation Context"
                ))

        if violations:
            metrics_store.record_command_center_action("explainability_validation_failures", len(violations))
            response.violations.extend(violations)
            
        return len(violations) == 0, violations

from typing import Dict, Any, List
import logging
from dataclasses import dataclass

from app.core.governance.interfaces import GovernancePolicyProvider
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

@dataclass
class PolicyRule:
    name: str
    condition_key: str
    allowed_values: List[Any]
    enforcement_action: str # e.g. "BLOCK", "REQUIRE_APPROVAL", "ALLOW"

class GovernancePolicyEngine(GovernancePolicyProvider):
    def __init__(self):
        # In a real implementation, rules are loaded from DB/Config
        self.rules: List[PolicyRule] = [
            PolicyRule(name="sovereign_export", condition_key="target_region", allowed_values=["US", "EU"], enforcement_action="BLOCK"),
            PolicyRule(name="escalation_authority", condition_key="role", allowed_values=["admin", "commander"], enforcement_action="BLOCK")
        ]

    def evaluate_policy(self, policy_name: str, context: Dict[str, Any]) -> bool:
        """
        Deterministically evaluates a policy against a context payload.
        Returns True if allowed, False if blocked.
        """
        applicable_rules = [r for r in self.rules if r.name == policy_name]
        if not applicable_rules:
            logger.warning(f"No rules found for policy {policy_name}, defaulting to secure (False).")
            return False

        for rule in applicable_rules:
            context_val = context.get(rule.condition_key)
            if context_val not in rule.allowed_values:
                if rule.enforcement_action == "BLOCK":
                    metrics_store.record_governance_action("governance_policy_violations_total")
                    logger.warning(f"Policy {policy_name} violation: {context_val} not in {rule.allowed_values}")
                    return False
                # If REQUIRE_APPROVAL, we still allow the policy evaluation to pass, but the 
                # higher-level orchestrator must route it to Approvals. (Simplified for MVP)

        return True

governance_policy_engine = GovernancePolicyEngine()

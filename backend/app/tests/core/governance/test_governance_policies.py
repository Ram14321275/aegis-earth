import pytest
from app.core.governance.policies.engine import GovernancePolicyEngine

def test_governance_policy_evaluation():
    engine = GovernancePolicyEngine()
    
    # Test valid export
    context_valid = {"target_region": "US"}
    assert engine.evaluate_policy("sovereign_export", context_valid) is True
    
    # Test blocked export
    context_invalid = {"target_region": "CN"}
    assert engine.evaluate_policy("sovereign_export", context_invalid) is False
    
    # Test escalation authority
    assert engine.evaluate_policy("escalation_authority", {"role": "admin"}) is True
    assert engine.evaluate_policy("escalation_authority", {"role": "operator"}) is False

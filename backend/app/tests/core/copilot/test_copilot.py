import pytest
from app.core.copilot.models import (
    ThreatSummary, CopilotRecommendation, ConfidenceAssessment, 
    ConfidenceLevel, RecommendationImpact, RecommendationRollback,
    CopilotResponse, MissionNarrative, NarrativeType, CopilotReasoningTrace
)
from app.core.copilot.explainability.validator import ExplainabilityValidator
from app.core.copilot.governance.policy import GovernanceEngine
from app.core.copilot.narratives.engine import DeterministicNarrativeEngine
from app.core.copilot.models import MissionContext

@pytest.fixture
def governance_engine():
    return GovernanceEngine()

@pytest.fixture
def validator():
    return ExplainabilityValidator()

@pytest.fixture
def narrative_engine():
    return DeterministicNarrativeEngine()


def test_governance_blocks_destructive_actions(governance_engine):
    rec = CopilotRecommendation(
        id="test-1",
        action_type="destroy_server",
        title="Destroy Server",
        rationale="Server is compromised.",
        evidence_chain=["Log data"],
        operational_severity="HIGH",
        confidence=ConfidenceAssessment(score=0.9, level=ConfidenceLevel.HIGH, explanation="Testing"),
        impact=RecommendationImpact(resource_cost="HIGH", time_to_implement="IMMEDIATE", expected_outcome="Destruction"),
        rollback=RecommendationRollback(strategy="None", time_to_rollback="NONE", complexity="NONE")
    )
    result = governance_engine.evaluate(rec)
    assert not result.governance_review.approved
    assert "Destructive infrastructure actions" in result.governance_review.policy_violations[0]


def test_governance_enforces_confidence_thresholds(governance_engine):
    rec = CopilotRecommendation(
        id="test-2",
        action_type="increase_monitoring",
        title="Increase Monitoring",
        rationale="Possible threat.",
        evidence_chain=["Sensors"],
        operational_severity="CRITICAL",
        confidence=ConfidenceAssessment(score=0.5, level=ConfidenceLevel.MODERATE, explanation="Testing"),
        impact=RecommendationImpact(resource_cost="LOW", time_to_implement="IMMEDIATE", expected_outcome="Monitoring"),
        rollback=RecommendationRollback(strategy="None", time_to_rollback="NONE", complexity="NONE")
    )
    result = governance_engine.evaluate(rec)
    # Severity should be degraded to MODERATE because score is 0.5
    assert result.operational_severity == "MODERATE"
    assert "CRITICAL severity requires confidence >= 0.9" in result.governance_review.policy_violations[0]


def test_explainability_validator_missing_hash(validator):
    trace = CopilotReasoningTrace(
        trace_id="trace-1",
        tenant_id="tenant-1",
        source_systems=["system-1"],
        reasoning_hash="",
        evidence_hash="12345"
    )
    narrative = MissionNarrative(
        narrative_type=NarrativeType.SHORT_SUMMARY,
        content="Test narrative",
        trace=trace
    )
    response = CopilotResponse(
        response_id="resp-1",
        tenant_id="tenant-1",
        mission_id="mission-1",
        narrative=narrative,
        recommendations=[],
        insights=[],
        threats=[],
        trace=trace
    )
    
    is_valid, violations = validator.validate(response)
    assert not is_valid
    assert any(v.violation_type == "MISSING_REASONING_HASH" for v in violations)


def test_explainability_validator_missing_evidence(validator):
    trace = CopilotReasoningTrace(
        trace_id="trace-1",
        tenant_id="tenant-1",
        source_systems=["system-1"],
        reasoning_hash="hash",
        evidence_hash="hash"
    )
    rec = CopilotRecommendation(
        id="test-1",
        action_type="action",
        title="Action",
        rationale="Rationale",
        evidence_chain=[], # Empty evidence
        operational_severity="LOW",
        confidence=ConfidenceAssessment(score=0.9, level=ConfidenceLevel.HIGH, explanation="Test"),
        impact=RecommendationImpact(resource_cost="LOW", time_to_implement="IMMEDIATE", expected_outcome="Test"),
        rollback=RecommendationRollback(strategy="None", time_to_rollback="NONE", complexity="NONE")
    )
    
    narrative = MissionNarrative(
        narrative_type=NarrativeType.SHORT_SUMMARY,
        content="Test narrative",
        trace=trace
    )
    
    response = CopilotResponse(
        response_id="resp-1",
        tenant_id="tenant-1",
        mission_id="mission-1",
        narrative=narrative,
        recommendations=[rec],
        insights=[],
        threats=[ThreatSummary(hazard_type="TEST", severity="LOW", affected_area="Area", estimated_impact="Impact")], # Add a threat to avoid orphaned violation
        trace=trace
    )
    
    is_valid, violations = validator.validate(response)
    assert not is_valid
    assert any(v.violation_type == "MISSING_EVIDENCE" for v in violations)


def test_deterministic_narrative_generation(narrative_engine):
    context = MissionContext(
        mission_id="m1",
        tenant_id="t1",
        region_id="r1",
        infrastructure_status="OPERATIONAL"
    )
    trace = CopilotReasoningTrace(
        trace_id="trace-1",
        tenant_id="t1",
        source_systems=["system-1"],
        reasoning_hash="",
        evidence_hash="hash"
    )
    threat = ThreatSummary(
        hazard_type="FLOOD",
        severity="CRITICAL",
        affected_area="Downtown",
        estimated_impact="High water levels"
    )
    
    narrative = narrative_engine.generate_short_summary(context, [threat], trace)
    
    # Must be deterministic and reproduce the exact same hash
    assert narrative.trace.reasoning_hash != ""
    hash1 = narrative.trace.reasoning_hash
    
    narrative2 = narrative_engine.generate_short_summary(context, [threat], trace)
    assert narrative2.trace.reasoning_hash == hash1

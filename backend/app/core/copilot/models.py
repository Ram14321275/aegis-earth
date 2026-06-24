from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CopilotDegradationMode(str, Enum):
    FULL_INTELLIGENCE = "FULL_INTELLIGENCE"
    PARTIAL_PREDICTIVE_LOSS = "PARTIAL_PREDICTIVE_LOSS"
    TELEMETRY_STALE = "TELEMETRY_STALE"
    MEMORY_DEGRADED = "MEMORY_DEGRADED"
    PROVIDER_DEGRADED = "PROVIDER_DEGRADED"
    SAFE_FALLBACK = "SAFE_FALLBACK"


class NarrativeType(str, Enum):
    SHORT_SUMMARY = "SHORT_SUMMARY"
    DETAILED_REPORT = "DETAILED_REPORT"
    EXECUTIVE_DIGEST = "EXECUTIVE_DIGEST"
    ESCALATION_REPORT = "ESCALATION_REPORT"


class ConfidenceLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ConfidenceAssessment(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0)
    level: ConfidenceLevel
    explanation: str


class MissionContext(BaseModel):
    mission_id: str
    tenant_id: str
    region_id: Optional[str] = None
    hazard_types: List[str] = []
    active_threats: List[str] = []
    infrastructure_status: str
    timestamp: datetime = Field(default_factory=get_utc_now)


class OperationalInsight(BaseModel):
    insight_type: str
    description: str
    source_systems: List[str]
    confidence_assessment: ConfidenceAssessment


class ThreatSummary(BaseModel):
    hazard_type: str
    severity: str
    affected_area: str
    estimated_impact: str


class RecommendationImpact(BaseModel):
    resource_cost: str
    time_to_implement: str
    expected_outcome: str


class RecommendationRollback(BaseModel):
    strategy: str
    time_to_rollback: str
    complexity: str


class GovernanceDecision(BaseModel):
    approved: bool
    rejection_reason: Optional[str] = None
    policy_violations: List[str] = []
    adjusted_severity: Optional[str] = None


class CopilotRecommendation(BaseModel):
    id: str
    action_type: str
    title: str
    rationale: str
    evidence_chain: List[str]
    operational_severity: str
    confidence: ConfidenceAssessment
    impact: RecommendationImpact
    rollback: RecommendationRollback
    governance_review: Optional[GovernanceDecision] = None
    generated_at: datetime = Field(default_factory=get_utc_now)


class ExplainabilityViolation(BaseModel):
    violation_type: str
    description: str
    failed_claim: str
    timestamp: datetime = Field(default_factory=get_utc_now)


class CopilotReasoningTrace(BaseModel):
    trace_id: str
    tenant_id: str
    generated_at: datetime = Field(default_factory=get_utc_now)
    source_systems: List[str]
    reasoning_hash: str
    evidence_hash: str
    source_snapshot_id: Optional[str] = None
    degradation_mode: CopilotDegradationMode = CopilotDegradationMode.FULL_INTELLIGENCE
    degraded_reason: Optional[str] = None


class EscalationNarrative(BaseModel):
    escalation_reason: str
    previous_severity: str
    new_severity: str
    causal_factors: List[str]


class IntelligenceDigest(BaseModel):
    key_findings: List[str]
    primary_concerns: List[str]
    notable_anomalies: List[str]


class MissionNarrative(BaseModel):
    narrative_type: NarrativeType
    content: str
    escalation_context: Optional[EscalationNarrative] = None
    digest: Optional[IntelligenceDigest] = None
    trace: CopilotReasoningTrace


class MissionMemoryRecord(BaseModel):
    thread_id: str
    tenant_id: str
    mission_id: str
    timestamp: datetime = Field(default_factory=get_utc_now)
    record_type: str
    content: Dict[str, Any]
    source_systems: List[str]
    annotations: List[str] = []


class CopilotResponse(BaseModel):
    response_id: str
    tenant_id: str
    mission_id: str
    generated_at: datetime = Field(default_factory=get_utc_now)
    narrative: MissionNarrative
    recommendations: List[CopilotRecommendation]
    insights: List[OperationalInsight]
    threats: List[ThreatSummary]
    trace: CopilotReasoningTrace
    violations: List[ExplainabilityViolation] = []

import time
import hashlib
from typing import List

from app.core.copilot.models import (
    MissionContext, MissionNarrative, ThreatSummary, 
    OperationalInsight, CopilotReasoningTrace, NarrativeType,
    EscalationNarrative, IntelligenceDigest
)
from app.core.copilot.interfaces.narrative import NarrativeEngineInterface
from app.observability.metrics import metrics_store


class DeterministicNarrativeEngine(NarrativeEngineInterface):
    """
    Deterministic template-driven narrative engine.
    Ensures 100% reproducibility and explainability. NO LLMs.
    """

    def _hash_content(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def generate_short_summary(
        self, context: MissionContext, threats: List[ThreatSummary], trace: CopilotReasoningTrace
    ) -> MissionNarrative:
        start_time = time.time()
        
        threat_count = len(threats)
        region = context.region_id or 'Unknown Region'
        
        content = f"Mission {context.mission_id} in {region}. "
        if threat_count > 0:
            primary_threat = sorted(threats, key=lambda t: self._severity_weight(t.severity), reverse=True)[0]
            content += f"Active threats detected ({threat_count}). Primary concern: {primary_threat.severity} {primary_threat.hazard_type}. "
        else:
            content += "No active threats detected. "
            
        content += f"Infrastructure status: {context.infrastructure_status}."
        
        trace.reasoning_hash = self._hash_content(content)
        
        narrative = MissionNarrative(
            narrative_type=NarrativeType.SHORT_SUMMARY,
            content=content,
            trace=trace
        )
        
        self._record_metrics(start_time)
        return narrative

    def generate_detailed_report(
        self, context: MissionContext, threats: List[ThreatSummary], 
        insights: List[OperationalInsight], trace: CopilotReasoningTrace
    ) -> MissionNarrative:
        start_time = time.time()
        
        region = context.region_id or 'Unknown Region'
        content = f"Detailed Operational Report for Mission {context.mission_id} ({region}).\n\n"
        
        content += "THREATS:\n"
        for t in threats:
            content += f"- {t.severity} {t.hazard_type}: {t.affected_area}. Impact: {t.estimated_impact}\n"
            
        content += "\nINSIGHTS:\n"
        for i in insights:
            content += f"- [{i.confidence_assessment.level}] {i.description} (Sources: {', '.join(i.source_systems)})\n"
            
        content += f"\nINFRASTRUCTURE: {context.infrastructure_status}"
        
        trace.reasoning_hash = self._hash_content(content)
        
        narrative = MissionNarrative(
            narrative_type=NarrativeType.DETAILED_REPORT,
            content=content,
            trace=trace
        )
        
        self._record_metrics(start_time)
        return narrative

    def generate_executive_digest(
        self, context: MissionContext, threats: List[ThreatSummary], trace: CopilotReasoningTrace
    ) -> MissionNarrative:
        start_time = time.time()
        
        high_threats = [t for t in threats if self._severity_weight(t.severity) >= 3]
        
        content = f"Executive Digest: Mission {context.mission_id}.\n"
        content += f"Critical/High Threats: {len(high_threats)}.\n"
        
        digest = IntelligenceDigest(
            key_findings=[f"{len(threats)} total threats active."],
            primary_concerns=[f"{t.hazard_type} in {t.affected_area}" for t in high_threats],
            notable_anomalies=[]
        )
        
        trace.reasoning_hash = self._hash_content(content)
        
        narrative = MissionNarrative(
            narrative_type=NarrativeType.EXECUTIVE_DIGEST,
            content=content,
            digest=digest,
            trace=trace
        )
        
        self._record_metrics(start_time)
        return narrative

    def generate_escalation_report(
        self, context: MissionContext, threats: List[ThreatSummary], trace: CopilotReasoningTrace
    ) -> MissionNarrative:
        start_time = time.time()
        
        primary_threat = sorted(threats, key=lambda t: self._severity_weight(t.severity), reverse=True)[0] if threats else None
        
        content = f"EMERGENCY ESCALATION: Mission {context.mission_id}.\n"
        escalation_context = None
        
        if primary_threat:
            content += f"Escalating due to {primary_threat.severity} {primary_threat.hazard_type}.\n"
            escalation_context = EscalationNarrative(
                escalation_reason=f"Detection of {primary_threat.severity} {primary_threat.hazard_type}",
                previous_severity="UNKNOWN",
                new_severity=primary_threat.severity,
                causal_factors=[primary_threat.estimated_impact]
            )
        else:
            content += "Escalation requested without explicit threat context.\n"
            
        trace.reasoning_hash = self._hash_content(content)
        
        narrative = MissionNarrative(
            narrative_type=NarrativeType.ESCALATION_REPORT,
            content=content,
            escalation_context=escalation_context,
            trace=trace
        )
        
        self._record_metrics(start_time)
        return narrative

    def _severity_weight(self, severity: str) -> int:
        mapping = {"LOW": 1, "MODERATE": 2, "HIGH": 3, "CRITICAL": 4}
        return mapping.get(severity.upper(), 0)

    def _record_metrics(self, start_time: float):
        duration = (time.time() - start_time) * 1000
        metrics_store.record_command_center_action("copilot_narratives_generated_total")
        metrics_store.record_command_center_action("narrative_generation_duration_ms", duration)

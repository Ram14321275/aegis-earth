from abc import ABC, abstractmethod
from typing import List
from app.core.copilot.models import (
    MissionContext, MissionNarrative, ThreatSummary, 
    OperationalInsight, CopilotReasoningTrace
)

class NarrativeEngineInterface(ABC):
    """Abstract interface for Narrative Generation."""

    @abstractmethod
    def generate_short_summary(
        self, context: MissionContext, threats: List[ThreatSummary], trace: CopilotReasoningTrace
    ) -> MissionNarrative:
        pass

    @abstractmethod
    def generate_detailed_report(
        self, context: MissionContext, threats: List[ThreatSummary], 
        insights: List[OperationalInsight], trace: CopilotReasoningTrace
    ) -> MissionNarrative:
        pass

    @abstractmethod
    def generate_executive_digest(
        self, context: MissionContext, threats: List[ThreatSummary], trace: CopilotReasoningTrace
    ) -> MissionNarrative:
        pass

    @abstractmethod
    def generate_escalation_report(
        self, context: MissionContext, threats: List[ThreatSummary], trace: CopilotReasoningTrace
    ) -> MissionNarrative:
        pass

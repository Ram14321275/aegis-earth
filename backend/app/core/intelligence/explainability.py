import time
from typing import List

from app.core.intelligence.models import (
    IntelligenceSignal, CorrelatedHazard, IntelligenceExplanation
)
from app.core.intelligence.interfaces import AIProvider
from app.observability.metrics import metrics_store


class DummyAIProvider(AIProvider):
    """
    Temporary placeholder AI provider.
    Replaced dynamically via Dependency Injection in production.
    """
    async def generate_explanation(
        self, signals: List[IntelligenceSignal], correlations: List[CorrelatedHazard]
    ) -> IntelligenceExplanation:
        
        indicators = [s.hazard_type.value for s in signals]
        
        if correlations:
            summary = f"Detected cascading environmental risks involving {len(correlations)} correlated factors."
            env_changes = [c.description for c in correlations]
        else:
            summary = f"Isolated hazard detected with high confidence."
            env_changes = [f"Localized {s.hazard_type.value} anomaly." for s in signals]
            
        return IntelligenceExplanation(
            contributing_indicators=list(set(indicators)),
            reasoning_summary=summary,
            confidence_explanation="Based on multi-spectral Earth Engine indices and temporal baselines.",
            detected_environmental_changes=env_changes
        )


class ExplainabilityEngine:
    def __init__(self, provider: AIProvider = None):
        # Default to Dummy if no provider is injected
        self.provider = provider or DummyAIProvider()
        
    async def generate(
        self, signals: List[IntelligenceSignal], correlations: List[CorrelatedHazard]
    ) -> IntelligenceExplanation:
        """
        Orchestrates the generation of explainable insights from raw intelligence signals.
        """
        start_time = time.time()
        
        try:
            explanation = await self.provider.generate_explanation(signals, correlations)
            return explanation
        finally:
            duration_ms = (time.time() - start_time) * 1000.0
            metrics_store.record_explainability_generation(duration_ms)

explainability_engine = ExplainabilityEngine()

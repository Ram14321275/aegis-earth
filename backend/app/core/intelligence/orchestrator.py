import uuid
import logging
from typing import List, Optional

from app.core.intelligence.models import (
    IntelligenceSignal, IntelligenceAssessment
)
from app.core.intelligence.correlation import cross_hazard_correlation_engine
from app.core.intelligence.explainability import explainability_engine
from app.core.intelligence.prioritization import event_prioritization_engine
from app.core.intelligence.metrics import intelligence_metrics

logger = logging.getLogger(__name__)

class UnifiedIntelligenceOrchestrator:
    @staticmethod
    async def aggregate(
        signals: List[IntelligenceSignal], 
        location_id: Optional[str] = None
    ) -> IntelligenceAssessment:
        """
        Transforms isolated hazard outputs into a unified planetary intelligence assessment.
        Delegates to prioritization, correlation, and AI explainability engines.
        """
        try:
            if not signals:
                logger.warning("No intelligence signals provided to orchestrator.")
                
            # 1. Correlate Signals (Cross-Hazard Reasoning)
            correlations = cross_hazard_correlation_engine.correlate(signals)
            
            # 2. Prioritize Signals (Rank by Severity/Area/Confidence)
            prioritized = event_prioritization_engine.prioritize(signals)
            
            # 3. Generate Explainability Summaries (AI Provider Integration)
            explanation = await explainability_engine.generate(signals, correlations)
            
            # Record successful aggregation
            intelligence_metrics.record_aggregation()
            
            # Calculate overarching confidence and severity
            max_confidence = max([s.confidence for s in signals]) if signals else 0.0
            
            severities = [s.severity for s in signals]
            from app.schemas.intelligence import SeverityEnum
            
            if SeverityEnum.CRITICAL in severities:
                overall_severity = SeverityEnum.CRITICAL
            elif SeverityEnum.HIGH in severities:
                overall_severity = SeverityEnum.HIGH
            elif SeverityEnum.MEDIUM in severities:
                overall_severity = SeverityEnum.MEDIUM
            else:
                overall_severity = SeverityEnum.LOW

            # 4. Construct Assessment
            return IntelligenceAssessment(
                assessment_id=f"intel_{uuid.uuid4()}",
                location_id=location_id,
                signals=signals,
                correlations=correlations,
                prioritized_events=prioritized,
                explainability=explanation,
                forecasts=[],  # To be populated by future ML forecasting integrations
                source=["UnifiedIntelligenceOrchestrator"],
                confidence=max_confidence,
                severity=overall_severity,
                analysis_version="1.0"
            )
            
        except Exception as e:
            intelligence_metrics.record_failure()
            logger.error(f"Intelligence Orchestration failed: {str(e)}")
            raise e

unified_intelligence_orchestrator = UnifiedIntelligenceOrchestrator()

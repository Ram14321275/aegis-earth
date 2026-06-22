import logging
import uuid
from datetime import datetime
from app.core.predictive.remediation.models import (
    RemediationPlan, AutonomousDecision, RecoveryWorkflow, RemediationAction
)
from app.core.predictive.infrastructure.models import InfrastructureForecast
from app.core.predictive.explainability.contracts import Explanation, ContributingSignal

logger = logging.getLogger(__name__)

class AutonomousRemediationEngine:
    """
    Triggers safe remediation workflows and recommends scaling actions.
    Must never execute destructive actions automatically without rollback plans.
    """

    async def evaluate_infrastructure_forecast(self, forecast: InfrastructureForecast) -> RemediationPlan:
        """
        Takes an infrastructure forecast and generates a remediation plan.
        MVP: Only logs recommendations, does not execute destructively.
        """
        decisions = []
        
        # Check queue saturation risk
        for qf in forecast.queue_forecasts:
            if qf.saturation_risk > 0.15:
                workflow = RecoveryWorkflow(
                    workflow_id=str(uuid.uuid4()),
                    steps=[
                        RemediationAction(action_type="SCALE_WORKERS", target=qf.queue_name, parameters={"replicas": "+2"})
                    ],
                    rollback_steps=[
                        RemediationAction(action_type="SCALE_WORKERS", target=qf.queue_name, parameters={"replicas": "-2"})
                    ]
                )
                
                decision = AutonomousDecision(
                    decision_id=str(uuid.uuid4()),
                    timestamp=datetime.utcnow(),
                    trigger_source=f"QueuePressureForecast:{qf.queue_name}",
                    recommended_workflow=workflow,
                    explainability=Explanation(
                        contributing_factors=[
                            ContributingSignal(
                                source="infrastructure.queue_forecast",
                                weight=1.0,
                                impact=f"Saturation risk {qf.saturation_risk}",
                                timestamp=datetime.utcnow().isoformat()
                            )
                        ],
                        weighted_reasoning="Queue depth is increasing towards saturation. Scaling workers will alleviate pressure.",
                        confidence_explanation="High confidence based on deterministic queue metrics.",
                        uncertainty_explanation="Spike duration is unknown.",
                        degraded_mode_active=False
                    ),
                    is_executed_automatically=False, # Safety constraint
                    status="PENDING"
                )
                decisions.append(decision)
                logger.info(f"Generated remediation decision: {decision.decision_id} for queue {qf.queue_name}")

        plan = RemediationPlan(
            plan_id=str(uuid.uuid4()),
            decisions=decisions,
            overall_risk_reduction="MODERATE" if decisions else "NONE"
        )
        return plan

autonomous_remediation_engine = AutonomousRemediationEngine()

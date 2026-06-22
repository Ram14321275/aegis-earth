import logging
import uuid
import time
from datetime import datetime
from app.core.predictive.simulation.models import (
    ScenarioSimulation, RegionalImpactProjection, CascadeProjection, EnvironmentalTrajectory
)
from app.core.predictive.explainability.contracts import Explanation, ContributingSignal
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class SimulationEngine:
    """
    Simulates hazard cascades and environmental trajectories.
    Exposes all reasoning transparently.
    """

    async def run_simulation(self, tenant_id: str, scenario_name: str, horizon_hours: int) -> ScenarioSimulation:
        """
        Executes a deterministic simulation.
        In a real scenario, this would trigger background workers to perform heavy geospatial modeling.
        """
        start_time = time.time()
        
        # Mock projection
        impact = RegionalImpactProjection(
            region_id="sector-7g",
            impacted_population=15000,
            infrastructure_damage_estimate="MODERATE",
            projected_severity=0.65
        )
        
        cascade = CascadeProjection(
            cascade_id=str(uuid.uuid4()),
            trigger_hazard="wildfire",
            resultant_hazards=["air_quality_degradation", "power_outage"],
            timeline_offset_hours=48
        )
        
        trajectory = EnvironmentalTrajectory(
            trajectory_id=str(uuid.uuid4()),
            parameters={"wind_shift_probability": 0.3, "precipitation_chance": 0.1}
        )
        
        explanation = Explanation(
            contributing_factors=[
                ContributingSignal(
                    source="wildfire_spread_model",
                    weight=0.9,
                    impact="Dry fuel loads and wind vectors strongly suggest northeast spread.",
                    timestamp=datetime.utcnow().isoformat()
                )
            ],
            weighted_reasoning="Northeast spread intersects with power infrastructure, cascading to outages.",
            confidence_explanation="High confidence in fire spread, moderate confidence in power grid resilience.",
            uncertainty_explanation="Wind direction changes could alter trajectory significantly.",
            degraded_mode_active=False
        )

        simulation = ScenarioSimulation(
            simulation_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            scenario_name=scenario_name,
            executed_at=datetime.utcnow(),
            horizon_hours=horizon_hours,
            regional_impacts=[impact],
            cascades=[cascade],
            trajectories=[trajectory],
            explainability=explanation
        )
        
        duration_ms = (time.time() - start_time) * 1000
        metrics_store.record_command_center_action("simulation_duration_ms", duration_ms)
        logger.info(f"Completed simulation {simulation.simulation_id} in {duration_ms:.2f}ms")
        
        return simulation

simulation_engine = SimulationEngine()

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from app.core.economics.forecasting.engine import economic_forecasting_engine
from app.core.economics.logistics.router import logistics_router
from app.core.economics.allocation.engine import resource_allocation_engine
from app.core.economics.sovereignty.trade import sovereign_trade_engine
from app.core.economics.stabilization.engine import economic_stabilization_engine
from app.core.economics.disruption.engine import economic_disruption_engine
from app.core.economics.markets.engine import market_signal_engine
from app.core.economics.simulation.engine import economic_simulation_engine
from app.core.economics.orchestration.engine import economic_orchestrator
from app.core.economics.lineage.tracker import resource_lineage_tracker

router = APIRouter(prefix="/economics", tags=["economics"])

@router.post("/forecasting")
async def generate_forecast(resource_type: str, current_stock: float, consumption_rate: float, inbound_supply: float):
    return economic_forecasting_engine.generate_shortfall_forecast(resource_type, current_stock, consumption_rate, inbound_supply)

@router.post("/logistics")
async def calculate_route(origin: str, destination: str, current_congestion: float):
    return logistics_router.calculate_corridor(origin, destination, current_congestion)

@router.post("/allocation")
async def allocate_resources(resource_type: str, total_available: float, requests: List[Dict[str, Any]]):
    return resource_allocation_engine.allocate_resources(resource_type, total_available, requests)

@router.post("/trade")
async def validate_trade(origin: str, destination: str, resource_type: str, active_restrictions: List[Dict[str, Any]]):
    valid = sovereign_trade_engine.validate_trade_route(origin, destination, resource_type, active_restrictions)
    if not valid:
        raise HTTPException(status_code=403, detail="Trade route blocked by sovereign restriction.")
    return {"status": "ALLOWED"}

@router.post("/stabilization")
async def recommend_stabilization(supply_instability: float, logistics_congestion: float, market_volatility: float):
    return economic_stabilization_engine.recommend_stabilization(supply_instability, logistics_congestion, market_volatility)

@router.post("/disruptions")
async def calculate_disruption(root_cause_severity: float, dependencies: int):
    return economic_disruption_engine.calculate_disruption(root_cause_severity, dependencies)

@router.post("/markets")
async def ingest_market_signal(signal_type: str, volatility: float, staleness_seconds: float):
    return market_signal_engine.ingest_signal(signal_type, volatility, staleness_seconds)

@router.post("/simulations")
async def run_simulation(scenario: str, parameters: Dict[str, Any]):
    res = await economic_simulation_engine.run_simulation(scenario, parameters)
    if res.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=res.get("reason"))
    return res

@router.post("/resilience")
async def run_resilience_orchestration(workflow_name: str, parameters: Dict[str, Any]):
    return economic_orchestrator.execute_economic_workflow(workflow_name, parameters)

@router.post("/lineage/validate")
async def validate_lineage(lineage_chain: List[Dict[str, Any]]):
    valid = resource_lineage_tracker.validate_lineage(lineage_chain)
    return {"valid": valid}

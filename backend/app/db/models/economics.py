from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Float, Boolean, Integer
from sqlalchemy.sql import func
from app.db.base import TenantAwareModel

class ResourceForecast(TenantAwareModel):
    __tablename__ = "resource_forecasts"
    forecast_id = Column(String, primary_key=True, index=True)
    resource_type = Column(String, nullable=False)
    projected_shortfall = Column(Float, nullable=False)
    reasoning_hash = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class SupplyChainEvent(TenantAwareModel):
    __tablename__ = "supply_chain_events"
    event_id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class InfrastructureDependency(TenantAwareModel):
    __tablename__ = "infrastructure_dependencies"
    dependency_id = Column(String, primary_key=True, index=True)
    source_node = Column(String, nullable=False)
    target_node = Column(String, nullable=False)
    criticality = Column(Float, nullable=False)

class ResourceAllocation(TenantAwareModel):
    __tablename__ = "resource_allocations"
    allocation_id = Column(String, primary_key=True, index=True)
    target_region = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    reasoning_hash = Column(String, nullable=False)

class LogisticsRoute(TenantAwareModel):
    __tablename__ = "logistics_routes"
    route_id = Column(String, primary_key=True, index=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    congestion_score = Column(Float, nullable=False)

class TradeRestriction(TenantAwareModel):
    __tablename__ = "trade_restrictions"
    restriction_id = Column(String, primary_key=True, index=True)
    source_region = Column(String, nullable=False)
    target_region = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    active = Column(Boolean, default=True)

class EconomicDisruption(TenantAwareModel):
    __tablename__ = "economic_disruptions"
    disruption_id = Column(String, primary_key=True, index=True)
    impact_score = Column(Float, nullable=False)
    cascading_depth = Column(Integer, nullable=False)
    lineage_reference = Column(String, nullable=False)

class StabilizationAction(TenantAwareModel):
    __tablename__ = "stabilization_actions"
    action_id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    reasoning_hash = Column(String, nullable=False)
    status = Column(String, default="PENDING")

class StrategicReserve(TenantAwareModel):
    __tablename__ = "strategic_reserves"
    reserve_id = Column(String, primary_key=True, index=True)
    region = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    current_capacity = Column(Float, nullable=False)

class MarketSignal(TenantAwareModel):
    __tablename__ = "market_signals"
    signal_id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    volatility = Column(Float, nullable=False)
    staleness_seconds = Column(Float, nullable=False)

class ResourceSimulation(TenantAwareModel):
    __tablename__ = "resource_simulations"
    simulation_id = Column(String, primary_key=True, index=True)
    scenario = Column(String, nullable=False)
    results = Column(JSON)

class AllocationApproval(TenantAwareModel):
    __tablename__ = "allocation_approvals"
    approval_id = Column(String, primary_key=True, index=True)
    allocation_id = Column(String, ForeignKey("resource_allocations.allocation_id"))
    status = Column(String, nullable=False)

class ResourceLineage(TenantAwareModel):
    __tablename__ = "resource_lineage"
    lineage_id = Column(String, primary_key=True, index=True)
    event_hash = Column(String, nullable=False)
    parent_hash = Column(String, nullable=False)

class EconomicViolation(TenantAwareModel):
    __tablename__ = "economic_violations"
    violation_id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    severity = Column(String, nullable=False)

class SovereignTradeBoundary(TenantAwareModel):
    __tablename__ = "sovereign_trade_boundaries"
    boundary_id = Column(String, primary_key=True, index=True)
    region_a = Column(String, nullable=False)
    region_b = Column(String, nullable=False)
    trade_allowed = Column(Boolean, nullable=False)

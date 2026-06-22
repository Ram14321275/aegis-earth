import uuid
from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends, Request

from app.gateway.contracts.public import IntelligenceSnapshot, ReliabilityMetadata
from app.gateway.deduplication import coalescer
from app.gateway.federation.orchestrator import federation_engine
from app.gateway.rate_limiting.limiter import public_rate_limit, tenant_rate_limit
from app.core.security.auth import get_current_user_optional

router = APIRouter(prefix="/intelligence", tags=["Intelligence Gateway"])


@router.post(
    "/query",
    response_model=IntelligenceSnapshot,
    dependencies=[Depends(tenant_rate_limit)],
)
async def query_intelligence(
    request: Request,
    payload: Dict[str, Any],
    user: Any = Depends(get_current_user_optional),
):
    """
    Unified entry point for global intelligence.
    Automatically coalesces identical in-flight requests and federates underlying hazard engines.
    """
    # 1. We wrap the heavy federation logic
    async def _execute_federation() -> Dict[str, Any]:
        return await federation_engine.orchestrate(payload)

    # 2. Pass it to the Request Coalescer
    # We use a static version for MVP, but normally this would be parsed from config or headers
    analysis_version = "1.0.0"
    provider_version = "v1"

    raw_result = await coalescer.execute_coalesced(
        payload, analysis_version, provider_version, _execute_federation
    )

    # 3. Construct the strict public contract
    # Normally we would parse raw_result['flood'] and raw_result['wildfire'] to populate these.
    # For now, we return a mock structured snapshot incorporating the reliability metadata.
    
    # Reconstruct reliability metadata if it was stringified by JSON (from coalescer)
    if isinstance(raw_result.get("reliability"), dict):
        reliability = ReliabilityMetadata(**raw_result["reliability"])
    else:
        reliability = ReliabilityMetadata(
            overall_confidence=1.0,
            degraded_providers=[],
            cache_hit=False,
            federation_latency_ms=0.0,
            data_staleness_seconds=0
        )

    return IntelligenceSnapshot(
        snapshot_id=str(uuid.uuid4()),
        generated_at=datetime.utcnow(),
        reliability=reliability,
        # Placeholder mapping
        regional_summary=None,
        global_map=None,
        coordinates=payload.get("coordinates")
    )

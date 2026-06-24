from fastapi import APIRouter

from app.api.v1.routes.geospatial import router as geospatial_router
from app.api.v1.routes import search, system, jobs, analysis, tiles, command_center, predictive, copilot, operations, integrations, governance, edge, cyber, resilience, economics
from app.gateway.router import router as gateway_router




api_v1_router = APIRouter()

api_v1_router.include_router(system.router)
api_v1_router.include_router(geospatial_router)
api_v1_router.include_router(search.router)
api_v1_router.include_router(jobs.router)
api_v1_router.include_router(analysis.router)
api_v1_router.include_router(gateway_router)
api_v1_router.include_router(tiles.router)
api_v1_router.include_router(command_center.router)
api_v1_router.include_router(predictive.router)
api_v1_router.include_router(copilot.router)
api_v1_router.include_router(operations.router)
api_v1_router.include_router(integrations.router)
api_v1_router.include_router(governance.router)
api_v1_router.include_router(edge.router)
api_v1_router.include_router(cyber.router)
api_v1_router.include_router(resilience.router)
api_v1_router.include_router(economics.router)

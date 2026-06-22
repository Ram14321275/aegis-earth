from fastapi import APIRouter

from app.api.v1.routes.geospatial import router as geospatial_router
from app.api.v1.routes import search, system, jobs, analysis, tiles, command_center
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



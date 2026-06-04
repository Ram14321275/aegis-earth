from fastapi import APIRouter

from app.api.v1.routes.geospatial import router as geospatial_router
from app.api.v1.routes import search, system, jobs

api_v1_router = APIRouter()

api_v1_router.include_router(system.router)
api_v1_router.include_router(geospatial_router)
api_v1_router.include_router(search.router)
api_v1_router.include_router(jobs.router)

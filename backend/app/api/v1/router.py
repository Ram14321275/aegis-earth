from fastapi import APIRouter

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.geospatial import router as geospatial_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router, tags=["system"])
api_v1_router.include_router(geospatial_router)

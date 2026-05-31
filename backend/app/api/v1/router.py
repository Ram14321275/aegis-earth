from fastapi import APIRouter

from app.api.v1.routes.geospatial import router as geospatial_router
from app.api.v1.routes.system import router as system_router
from app.api.v1.routes.search import router as search_router

api_v1_router = APIRouter()
api_v1_router.include_router(system_router, prefix="/system", tags=["system"])
api_v1_router.include_router(geospatial_router)
api_v1_router.include_router(search_router)

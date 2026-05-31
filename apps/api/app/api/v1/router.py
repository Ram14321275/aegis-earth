from fastapi import APIRouter

from app.api.v1.intelligence import router as intelligence_router

api_router = APIRouter()
api_router.include_router(intelligence_router, prefix="/intelligence", tags=["intelligence"])


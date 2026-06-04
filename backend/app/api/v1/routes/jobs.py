from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.core.jobs.models import JobCreate, JobResponse
from app.core.jobs.service import job_service

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("", response_model=JobResponse, status_code=201)
async def create_job(
    job_in: JobCreate,
    session: AsyncSession = Depends(get_db_session)
):
    return await job_service.create_job(session, job_in)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    session: AsyncSession = Depends(get_db_session)
):
    return await job_service.get_job(session, job_id)

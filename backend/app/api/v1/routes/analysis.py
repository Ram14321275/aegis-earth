from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.core.jobs.models import JobCreate, JobResponse
from app.core.jobs.orchestration import job_orchestrator

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_analysis_job(
    job_in: JobCreate,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Submits a new analysis job to the distributed processing queue.
    Supports idempotency via the `Idempotency-Key` header.
    Returns 202 Accepted immediately with a job ID.
    """
    return await job_orchestrator.handle_analysis_request(
        session=session, 
        create_data=job_in, 
        idempotency_key=idempotency_key
    )

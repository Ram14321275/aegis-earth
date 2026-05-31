from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.schemas.common import APIResponse, ErrorDetail
from app.core.logging import get_logger

logger = get_logger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("Validation error", extra={"errors": exc.errors(), "body": exc.body})
    error_detail = ErrorDetail(code="VALIDATION_ERROR", message="Invalid request parameters")
    return JSONResponse(
        status_code=422,
        content=APIResponse(error=error_detail).model_dump(exclude_none=True)
    )

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception occurred")
    error_detail = ErrorDetail(code="INTERNAL_SERVER_ERROR", message="An unexpected error occurred")
    return JSONResponse(
        status_code=500,
        content=APIResponse(error=error_detail).model_dump(exclude_none=True)
    )

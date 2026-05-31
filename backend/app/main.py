from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.exceptions import global_exception_handler, validation_exception_handler
from app.core.logging import configure_logging, get_logger
from app.core.security import build_security_headers
from app.middleware.request_context import RequestContextMiddleware
from app.observability.telemetry import TelemetryMiddleware

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging(settings.log_level)
    logger.info(
        "backend_started",
        extra={
            "service": settings.service_name,
            "version": settings.api_version,
            "environment": settings.environment,
        },
    )
    yield
    logger.info("backend_stopped", extra={"service": settings.service_name})


app = FastAPI(
    title=settings.service_name,
    version=settings.api_version,
    description="Aegis Earth disaster intelligence API foundation.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(RequestContextMiddleware, security_headers=build_security_headers())
app.add_middleware(TelemetryMiddleware)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(api_v1_router, prefix="/api/v1")


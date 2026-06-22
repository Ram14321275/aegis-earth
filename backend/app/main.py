from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.api.ws.router import ws_router
from app.core.config import get_settings
from app.core.exceptions import global_exception_handler, validation_exception_handler
from app.core.logging import configure_logging, get_logger
from app.core.security import build_security_headers
from app.middleware.request_context import RequestContextMiddleware
from app.observability.telemetry import TelemetryMiddleware
from app.core.security.middleware import AuthenticationMiddleware, TenantContextMiddleware, RBACMiddleware, AuditMiddleware

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
    from app.core.workers.service import worker_service
    from app.core.workers.scheduler import worker_scheduler
    from app.core.streaming.consumers import event_consumer
    
    await worker_service.start_workers(count=4)
    await worker_scheduler.start()
    await event_consumer.start()
    
    yield
    
    await event_consumer.stop()
    await worker_service.stop_workers()
    await worker_scheduler.stop()
    
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

# Security Middlewares (added in reverse order of execution, so Auth runs first)
app.add_middleware(AuditMiddleware)
app.add_middleware(RBACMiddleware)
app.add_middleware(TenantContextMiddleware)
app.add_middleware(AuthenticationMiddleware)

from app.core.exceptions import (
    global_exception_handler, 
    validation_exception_handler,
    NotFoundError,
    ValidationError as CustomValidationError,
    not_found_exception_handler,
    custom_validation_exception_handler
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(CustomValidationError, custom_validation_exception_handler)
app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(ws_router, prefix="/ws", tags=["streaming"])


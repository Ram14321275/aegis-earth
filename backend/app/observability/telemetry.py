import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.observability.metrics import metrics_store


class TelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            success = 200 <= response.status_code < 400
            metrics_store.record_api_request(
                success, (time.time() - start_time) * 1000
            )
            return response
        except Exception as e:
            metrics_store.record_api_request(False, (time.time() - start_time) * 1000)
            raise e

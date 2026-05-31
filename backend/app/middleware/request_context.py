from collections.abc import Awaitable, Callable, Mapping
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

RequestHandler = Callable[[Request], Awaitable[Response]]


class RequestContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, security_headers: Mapping[str, str]) -> None:  # type: ignore[no-untyped-def]
        super().__init__(app)
        self.security_headers = security_headers

    async def dispatch(self, request: Request, call_next: RequestHandler) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        for header, value in self.security_headers.items():
            response.headers.setdefault(header, value)

        return response


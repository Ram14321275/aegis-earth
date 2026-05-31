from types import MappingProxyType
from typing import Mapping

DEFAULT_SECURITY_HEADERS: Mapping[str, str] = MappingProxyType(
    {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }
)


def build_security_headers() -> Mapping[str, str]:
    return DEFAULT_SECURITY_HEADERS


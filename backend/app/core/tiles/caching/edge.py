import hashlib
import logging
from typing import Dict, Any

from fastapi import Response

logger = logging.getLogger(__name__)

class EdgeCacheManager:
    """
    Manages CDN-compatible HTTP Cache-Control headers for map tiles.
    Optimized for Cloudflare and Fastly.
    """

    @staticmethod
    def set_tile_cache_headers(response: Response, severity: str = "LOW", is_playback: bool = False, payload_bytes: bytes = b""):
        """
        Injects Cache-Control, ETag, and Vary headers into the FastAPI Response.
        """
        # ETag based on actual content
        etag = hashlib.md5(payload_bytes).hexdigest()
        response.headers["ETag"] = f'"{etag}"'
        
        # Tenant isolation
        response.headers["Vary"] = "X-Tenant-ID"

        if is_playback:
            # Playback data is immutable
            response.headers["Cache-Control"] = "public, max-age=86400, immutable"
            return

        severity = severity.upper()
        if severity == "CRITICAL":
            # 30s max age, but allow stale serving for 2m if backend is slow
            response.headers["Cache-Control"] = "public, max-age=30, stale-while-revalidate=120"
        elif severity == "HIGH":
            # 5m max age
            response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=600"
        else:
            # 6h max age for stable data
            response.headers["Cache-Control"] = "public, max-age=21600, stale-while-revalidate=86400"

edge_cache_manager = EdgeCacheManager()

import time
import logging
from typing import Optional
from fastapi import HTTPException, Request

from app.core.cache.redis_client import redis_client
from app.core.security.tenants import get_current_tenant_id

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Sliding-window rate limiter backed by Redis Sorted Sets (ZSET).
    Tenant-aware and API-key aware.
    """

    def __init__(self, limit: int = 100, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds

    async def __call__(self, request: Request):
        tenant_id = get_current_tenant_id()
        api_key = request.headers.get("X-API-Key")
        ip = request.client.host if request.client else "unknown"

        # Determine the finest grain identifier
        if tenant_id:
            identifier = f"tenant:{tenant_id}"
        elif api_key:
            identifier = f"apikey:{api_key}"
        else:
            identifier = f"ip:{ip}"

        key = f"rate_limit:{identifier}"
        now = time.time()
        window_start = now - self.window_seconds

        client = await redis_client.get_client()
        if not client:
            logger.warning("Redis unavailable, bypassing rate limit.")
            return True

        # Pipeline to ensure atomicity
        async with client.pipeline(transaction=True) as pipe:
            try:
                # Remove elements older than window
                pipe.zremrangebyscore(key, 0, window_start)
                # Count current elements
                pipe.zcard(key)
                # Add current request
                pipe.zadd(key, {str(now): now})
                # Set expire on the key
                pipe.expire(key, self.window_seconds)
                
                results = await pipe.execute()
                
                # results[1] is the output of zcard
                current_count = results[1]
                
                if current_count >= self.limit:
                    raise HTTPException(
                        status_code=429,
                        detail={
                            "error": "Too Many Requests",
                            "message": f"Rate limit exceeded. Maximum {self.limit} requests per {self.window_seconds} seconds.",
                            "retry_after": self.window_seconds
                        },
                        headers={"Retry-After": str(self.window_seconds)}
                    )
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Rate limiting error: {e}")
                # Fail open to preserve availability if Redis hiccups
                return True

        return True


# Default instances
public_rate_limit = RateLimiter(limit=60, window_seconds=60)
tenant_rate_limit = RateLimiter(limit=600, window_seconds=60)

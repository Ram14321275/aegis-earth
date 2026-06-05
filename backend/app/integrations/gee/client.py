import asyncio
import logging
from typing import Callable, Any

from app.integrations.gee.auth import GEEAuthenticator
from app.integrations.gee.circuit_breaker import gee_circuit_breaker

logger = logging.getLogger(__name__)

class GEEClient:
    """
    Wraps GEE operations, enforcing authentication and offloading blocking IO to threads.
    """
    @staticmethod
    async def execute(func: Callable, *args, **kwargs) -> Any:
        if not gee_circuit_breaker.allow_request():
            raise RuntimeError("GEE Circuit Breaker is OPEN. Request denied.")
            
        if not GEEAuthenticator.is_authenticated():
            # Attempt to initialize on the fly if needed
            if not GEEAuthenticator.authenticate_and_initialize():
                raise RuntimeError("GEE is not authenticated and cannot execute queries.")

        try:
            # GEE python SDK is synchronous and makes HTTP calls. 
            # We MUST run it in a thread pool to avoid blocking the event loop.
            result = await asyncio.to_thread(func, *args, **kwargs)
            gee_circuit_breaker.record_success()
            return result
        except Exception as e:
            logger.error(f"GEE execution failed: {str(e)}")
            gee_circuit_breaker.record_failure()
            raise e

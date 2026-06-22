import time
import logging
from typing import Any, Callable, Coroutine
from enum import Enum

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Failing, reject requests immediately
    HALF_OPEN = "HALF_OPEN" # Testing recovery


class CircuitBreaker:
    """
    Prevents cascading failures by isolating degraded external or internal providers.
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_seconds: int = 60,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds

        self.state = CircuitState.CLOSED
        self.failures = 0
        self.last_failure_time = 0.0

    async def execute(self, action: Callable[[], Coroutine[Any, Any, Any]], fallback: Callable[[], Coroutine[Any, Any, Any]] = None) -> Any:
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout_seconds:
                logger.info(f"Circuit {self.name} entering HALF_OPEN state.")
                self.state = CircuitState.HALF_OPEN
            else:
                if fallback:
                    logger.warning(f"Circuit {self.name} is OPEN. Executing fallback.")
                    return await fallback()
                raise Exception(f"Circuit {self.name} is OPEN. Fast failing.")

        try:
            result = await action()
            if self.state == CircuitState.HALF_OPEN:
                logger.info(f"Circuit {self.name} recovered. State -> CLOSED.")
                self.state = CircuitState.CLOSED
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold and self.state != CircuitState.OPEN:
                logger.error(f"Circuit {self.name} threshold reached. State -> OPEN.")
                self.state = CircuitState.OPEN
            
            if fallback:
                logger.warning(f"Circuit {self.name} failed. Executing fallback. Error: {e}")
                return await fallback()
            raise

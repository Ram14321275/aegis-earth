import time
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    """
    Prevents repeated calls to an upstream service (GEE) when it is known to be failing.
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.last_failure_time = 0.0

    def record_success(self):
        """Records a successful operation."""
        if self.state != CircuitState.CLOSED:
            logger.info("Circuit Breaker reset to CLOSED.")
        self.state = CircuitState.CLOSED
        self.failures = 0

    def record_failure(self):
        """Records a failed operation."""
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            if self.state != CircuitState.OPEN:
                logger.warning(f"Circuit Breaker tripped OPEN after {self.failures} consecutive failures.")
            self.state = CircuitState.OPEN

    def allow_request(self) -> bool:
        """Determines if a request should be allowed through based on the current state."""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            now = time.time()
            if (now - self.last_failure_time) > self.recovery_timeout:
                logger.info("Circuit Breaker shifting to HALF_OPEN to test recovery.")
                self.state = CircuitState.HALF_OPEN
                return True
            return False
            
        if self.state == CircuitState.HALF_OPEN:
            # We only allow one request through while half open
            return False
            
        return True

# Global GEE Circuit Breaker
gee_circuit_breaker = CircuitBreaker()

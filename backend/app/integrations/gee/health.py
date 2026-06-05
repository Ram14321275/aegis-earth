import time
import ee
from app.integrations.gee.client import GEEClient
from app.integrations.gee.auth import GEEAuthenticator

async def check_gee_health() -> dict:
    """
    Executes a trivial operation on GEE servers to confirm bidirectional communication.
    Returns latency and availability metrics.
    """
    start_time = time.time()
    
    try:
        # A simple number initialization and evaluation requires hitting GEE REST APIs
        def ping():
            return ee.Number(1).getInfo()
            
        result = await GEEClient.execute(ping)
        
        latency = (time.time() - start_time) * 1000
        
        if result == 1:
            return {
                "status": "healthy",
                "authenticated": GEEAuthenticator.is_authenticated(),
                "collections_available": True,
                "latency_ms": round(latency, 2)
            }
        else:
            return {
                "status": "degraded",
                "authenticated": GEEAuthenticator.is_authenticated(),
                "collections_available": False,
                "latency_ms": round(latency, 2),
                "error": "Unexpected evaluation result"
            }
            
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        return {
            "status": "unhealthy",
            "authenticated": GEEAuthenticator.is_authenticated(),
            "collections_available": False,
            "latency_ms": round(latency, 2),
            "error": str(e)
        }

from datetime import datetime, timezone
import asyncio

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class HeartbeatSystem:
    def __init__(self, interval_seconds: int = 15):
        self.interval_seconds = interval_seconds
        
    async def run(self, worker_id: str, update_callback):
        try:
            while True:
                await asyncio.sleep(self.interval_seconds)
                update_callback(worker_id, get_utc_now())
        except asyncio.CancelledError:
            pass

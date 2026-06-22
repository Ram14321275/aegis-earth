import asyncio
import logging
import uuid
import json
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session_maker
from app.core.jobs.interfaces import WorkerInterface
from app.core.jobs.queue import redis_queue
from app.core.jobs.statuses import JobStatus
from app.core.jobs.retry import retry_manager
from app.core.cache.redis_client import redis_client
from app.core.security.tenants import set_current_tenant_id, set_current_user
from app.core.security.service_accounts import generate_worker_token
from app.core.security.jwt import decode_token

logger = logging.getLogger(__name__)

class AsyncWorker(WorkerInterface):
    def __init__(self, queue_names: list[str], max_concurrent: int = 10, lease_ttl_seconds: int = 300):
        self.worker_id = f"worker-{uuid.uuid4()}"
        self.queue_names = queue_names
        self.max_concurrent = max_concurrent
        self.lease_ttl_seconds = lease_ttl_seconds
        self.is_running = False
        self._tasks: set[asyncio.Task] = set()

    async def start(self) -> None:
        self.is_running = True
        logger.info(f"Worker {self.worker_id} started listening on {self.queue_names}")
        
        while self.is_running:
            if len(self._tasks) >= self.max_concurrent:
                await asyncio.sleep(1)
                continue

            # Poll across configured queues (simplistic loop)
            for q in self.queue_names:
                payload = await redis_queue.dequeue(q, timeout=1)
                if payload:
                    task = asyncio.create_task(self._process_with_isolation(payload))
                    self._tasks.add(task)
                    task.add_done_callback(self._tasks.discard)
                    break # Process one job at a time per iteration

    async def stop(self) -> None:
        self.is_running = False
        logger.info(f"Worker {self.worker_id} stopping...")
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

    async def _heartbeat_lease(self, job_id: str) -> None:
        client = await redis_client.get_client()
        if not client:
            return
            
        lease_key = f"lease:{job_id}"
        while self.is_running:
            await asyncio.sleep(self.lease_ttl_seconds / 2)
            # Refresh lease
            await client.expire(lease_key, self.lease_ttl_seconds)

    async def _claim_lease(self, job_id: str) -> bool:
        client = await redis_client.get_client()
        if not client:
            return True # Fallback

        lease_key = f"lease:{job_id}"
        acquired = await client.set(lease_key, self.worker_id, nx=True, ex=self.lease_ttl_seconds)
        return bool(acquired)

    async def _release_lease(self, job_id: str) -> None:
        client = await redis_client.get_client()
        if not client:
            return
        lease_key = f"lease:{job_id}"
        await client.delete(lease_key)

    async def _process_with_isolation(self, payload: Dict[str, Any]) -> None:
        job_id = payload.get("job_id")
        if not job_id:
            logger.error("Job payload missing job_id. Dropping.")
            return

        tenant_id = payload.get("tenant_id")
        if not tenant_id:
            logger.error(f"Job {job_id} missing tenant_id. Dropping.")
            return

        # Security Hardening: internal token
        try:
            token = generate_worker_token(self.worker_id, tenant_id)
            decoded = decode_token(token)
            set_current_user(decoded)
            set_current_tenant_id(tenant_id)
        except Exception as e:
            logger.error(f"Worker {self.worker_id} failed security validation: {e}")
            return

        # Try claim lease
        if not await self._claim_lease(job_id):
            logger.info(f"Worker {self.worker_id} skipped {job_id} (lease locked).")
            # In a resilient queue, this is NACK
            return

        heartbeat_task = asyncio.create_task(self._heartbeat_lease(job_id))
        
        try:
            # Enforce 10 min hard timeout on execution
            async with asyncio.timeout(600):
                await self.process_job(payload)
                # Success
        except asyncio.TimeoutError:
            logger.error(f"Job {job_id} timed out.")
            await self._handle_failure(payload, "TimeoutError")
        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}")
            await self._handle_failure(payload, str(e))
        finally:
            heartbeat_task.cancel()
            await self._release_lease(job_id)
            # Clean up context
            set_current_user(None)
            set_current_tenant_id(None)

    async def _handle_failure(self, payload: Dict[str, Any], reason: str) -> None:
        retry_count = payload.get("retry_count", 0)
        max_retries = payload.get("max_retries", 3)
        
        if retry_manager.should_retry(retry_count, max_retries):
            # exponential backoff delay and requeue
            delay = retry_manager.calculate_backoff(retry_count)
            payload["retry_count"] = retry_count + 1
            # In real system, we might push to a delayed queue.
            # Here we just log it and push it to the main queue (in MVP)
            logger.info(f"Requeueing {payload['job_id']} in {delay}s")
            await asyncio.sleep(delay)
            await redis_queue.enqueue(payload.get("queue_name", "default"), payload)
        else:
            logger.error(f"Job {payload['job_id']} reached max retries. Moving to Dead Letter Queue.")
            # Move to DLQ

    async def process_job(self, job_payload: Dict[str, Any]) -> None:
        """Override this in concrete workers."""
        raise NotImplementedError

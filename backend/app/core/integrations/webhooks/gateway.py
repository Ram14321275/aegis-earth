import logging
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException

from app.core.integrations.webhooks.security import WebhookSecurity
from app.core.integrations.ingestion.pipeline import ingestion_pipeline
from app.observability.metrics import metrics_store

logger = logging.getLogger(__name__)

class WebhookGateway:
    async def process_inbound(self, provider_id: str, request: Request, secret: str) -> Dict[str, str]:
        """
        Securely processes an inbound webhook request.
        """
        try:
            body = await request.body()
            signature = request.headers.get("x-signature") or request.headers.get("stripe-signature") # common headers
            
            if not signature:
                logger.warning(f"Missing signature for provider {provider_id}")
                raise HTTPException(status_code=401, detail="Missing signature")
                
            if not WebhookSecurity.verify_signature(body, signature, secret):
                logger.warning(f"Invalid signature for provider {provider_id}")
                raise HTTPException(status_code=401, detail="Invalid signature")

            payload = await request.json()
            
            # Send to async ingestion pipeline
            success, msg = await ingestion_pipeline.process_payload(provider_id, payload)
            
            if not success:
                logger.error(f"Ingestion failed for webhook from {provider_id}: {msg}")
                # We return 202 Accepted to the provider to avoid infinite retries on malformed payloads
                return {"status": "accepted", "message": "Payload quarantined"}

            return {"status": "success", "message": "Webhook processed"}
            
        except HTTPException:
            raise
        except Exception as e:
            metrics_store.record_command_center_action("webhook_failures_total")
            logger.error(f"Error processing webhook: {e}")
            raise HTTPException(status_code=500, detail="Internal processing error")

webhook_gateway = WebhookGateway()

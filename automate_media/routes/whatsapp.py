from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import logging


router = APIRouter()

# Load the verification token from environment variables
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")

@router.get("/webhook")
async def verify_webhook(request: Request):
    # Log the incoming request for debugging
    logging.info("Received verification request")
    logging.info(f"Query params: {request.query_params}")

    # Extract query parameters
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    # Verify the token
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    else:
        raise HTTPException(status_code=403, detail="Verification token mismatch")

@router.post("/webhook")
async def receive_message(request: Request):
    # Process incoming messages from WhatsApp
    data = await request.json()
    # Add your message processing logic here
    return {"status": "received"}



from fastapi import APIRouter, Request, HTTPException
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)

@router.get("/health")
async def health_check():
    return {"status": "healthyy"}

@router.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        logging.info(f"Received data: {data}")
        # Process the message...
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

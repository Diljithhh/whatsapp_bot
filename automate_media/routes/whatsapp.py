from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        if "messages" in data and data["messages"]:
            message = data["messages"][0]
            phone = message["from"]
            text = message["text"]["body"]
            # Handle WhatsApp message logic here...
            return JSONResponse(content={"status": "success"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# from fastapi import APIRouter, Request, HTTPException
# from fastapi.responses import JSONResponse
# from ..models.lead import Lead
# from ..services.firestore_service import save_lead
# from ..routes.whatsapp import get_bot_response

# router = APIRouter()


# @router.post("/api/chat")
# async def chat(request: Request):
#     try:
#         data = await request.json()
#         message = data.get("message")

#         # Use the same bot response logic we had before
#         bot_response = await get_bot_response(message)

#         return JSONResponse(content={
#             "status": "success",
#             "response": bot_response
#         })

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# routes/chat.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from ..models.lead import Lead
from ..services.firestore_service import save_lead
from ..main import AMDRetailerBot
from ..models.chatmodels import ChatRequest, ChatResponse

router = APIRouter()
bot = AMDRetailerBot()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if request.action == "welcome":
        if not request.customer_name:
            raise HTTPException(status_code=400, message="Customer name is required")
        return ChatResponse(
            message=f"Welcome onboard, {request.customer_name}! 👋\nI'm your AMD Retail Assistant, here to help you with your AMD product needs.",
            options={
                "services": {
                    "1": "Product Purchase",
                    "2": "Customer Support"
                }
            }
        )

    elif request.action == "get_categories":
        return ChatResponse(
            message="Please select a category:",
            options={"categories": bot.product_categories}
        )

    elif request.action == "get_products":
        if not request.selection in bot.product_categories.values():
            raise HTTPException(status_code=400, message="Invalid category")
        return ChatResponse(
            message=f"Available products in {request.selection}:",
            options={"products": bot.products.get(request.selection, [])}
        )

    else:
        raise HTTPException(status_code=400, message="Invalid action")

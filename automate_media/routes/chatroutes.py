# from fastapi import APIRouter, HTTPException
# from typing import Dict, Any

# from automate_media.services.chatservice import ChatService
# from automate_media.services.productservice import ProductService

# router = APIRouter()
# product_service = ProductService()


# @router.post("/chat/start")
# async def start_chat(customer_name: str) -> ChatMessage:
#     return chat_service.get_welcome_message(customer_name)

# @router.post("/chat/service")
# async def select_service(service_type: str) -> ChatMessage:
#     return chat_service.handle_service_selection(service_type)

# @router.post("/chat/category")
# async def select_category(category: str) -> ChatMessage:
#     return chat_service.handle_category_selection(category)
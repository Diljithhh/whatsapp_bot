# from typing import Dict, Any
# from automate_media.models.chatmodels import ChatMessage, ServiceType

# class ChatService:
#     def __init__(self, product_service):
#         self.product_service = product_service
#         self.conversation_states = {}

#     def get_welcome_message(self, customer_name: str) -> ChatMessage:
#         return ChatMessage(
#             message=f"Welcome onboard, {customer_name}! How can I assist you today?",
#             options=["Purchase", "Customer Support"]
#         )

#     def handle_service_selection(self, service_type: str) -> ChatMessage:
#         if service_type.lower() == "purchase":
#             categories = self.product_service.get_categories()
#             return ChatMessage(
#                 message="Please select a product category:",
#                 options=[cat.name for cat in categories]
#             )
#         else:
#             return ChatMessage(
#                 message="Our support team is here to help. What issue are you experiencing?",
#                 options=["Technical Support", "Order Status", "Returns", "Other"]
#             )

#     def handle_category_selection(self, category: str) -> ChatMessage:
#         products = self.product_service.get_products_by_category(category)
#         if not products:
#             return ChatMessage(
#                 message="No products found in this category.",
#                 options=["Select Another Category"]
#             )

#         product_options = [f"{p.name} - ${p.price}" for p in products]
#         return ChatMessage(
#             message=f"Here are the available products in {category}:",
#             options=product_options
#         )

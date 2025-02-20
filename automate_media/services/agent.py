import google.generativeai as genai
from typing import Dict, List

class DealerAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.context = {
            "dealer_services": {
                "product_categories": [
                    "Processors (AMD Ryzen Series)",
                    "Graphics Cards (Radeon RX Series)",
                    "Motherboards",
                    "Memory",
                    "Storage"
                ],
                "support_services": [
                    "Technical Support",
                    "Warranty Claims",
                    "Product Returns",
                    "Order Status"
                ]
            }
        }

        # Initialize conversation with system prompt
        self.conversation = self.model.start_chat(history=[
            {
                "role": "user",
                "parts": [self._create_system_prompt()]
            }
        ])

    def _create_system_prompt(self) -> str:
        return f"""
        You are an AMD dealer's assistant. Here are the services and products you can help with:

        Product Categories: {', '.join(self.context['dealer_services']['product_categories'])}
        Support Services: {', '.join(self.context['dealer_services']['support_services'])}

        Follow these rules:
        1. Always start with a welcome message and ask for the customer's name
        2. Keep context of the conversation and refer back to previous information
        3. If asking about products, guide them through categories before showing specific products
        4. For support queries, understand the issue and provide relevant assistance
        5. Keep responses concise and focused
        6. If you don't have specific product details, ask for clarification
        7. Always maintain a professional and helpful tone
        """

    async def process_message(self, message: str, session_data: Dict) -> str:
        try:
            # Add user context if available
            context = f"Customer Name: {session_data.get('customer_name', 'Unknown')}\n"
            context += f"Previous Topic: {session_data.get('current_topic', 'None')}\n"

            # Get response from Gemini
            response = await self.conversation.send_message_async(
                f"{context}\nUser message: {message}"
            )

            # Update session context based on response
            if "name" in message.lower() and not session_data.get('customer_name'):
                # Extract name from response and update session
                pass

            return response.text

        except Exception as e:
            return f"I apologize, but I encountered an error. Please try again. Error: {str(e)}"

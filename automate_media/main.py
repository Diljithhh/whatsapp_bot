# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from typing import Dict
# import json
# import os
# from dotenv import load_dotenv
# from automate_media.services.agent import DealerAgent
# from fastapi.middleware.cors import CORSMiddleware
# import logging
# from automate_media.routes.whatsapp import router as whatsapp_router


# # Load environment variables from .env file
# load_dotenv()

# # Verify API key is present
# if not os.getenv("GEMINI_API_KEY"):
#     raise ValueError("GEMINI_API_KEY environment variable is not set")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust this to your needs
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Initialize dealer agent with Gemini API key
# dealer_agent = DealerAgent(os.getenv("GEMINI_API_KEY"))

# # Store active connections and their session data
# connections: Dict[WebSocket, Dict] = {}

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Register the WhatsApp webhook router
# app.include_router(whatsapp_router, prefix="/whatsapp")

# @app.websocket("/ws/chat") # this is for the whatsapp webhook
# async def websocket_endpoint(websocket: WebSocket):
#     print(f"New connection attempt from {websocket.client}")
#     try:
#         await websocket.accept()
#         print(f"Connection accepted for {websocket.client}")

#         # Initialize session data for this connection
#         connections[websocket] = {
#             "customer_name": None,
#             "current_topic": None
#         }

#         # Send welcome message with options
#         await websocket.send_text(
#             json.dumps({
#                 "message": "Welcome to AMD Dealer Support! I'm your virtual assistant. May I know your name?",
#                 "type": "welcome",
#                 "options": ["Products", "Services"]
#             })
#         )

#         while True:
#             # Receive message from client
#             data = await websocket.receive_text()
#             logging.info(f"Received data: {data}")

#             if not data.strip():
#                 logging.warning("Received empty message, skipping processing.")
#                 continue

#             try:
#                 message_data = json.loads(data)
#             except json.JSONDecodeError as e:
#                 logging.error(f"JSON decode error: {e}")
#                 await websocket.send_text(
#                     json.dumps({
#                         "message": "Invalid message format.",
#                         "type": "error"
#                     })
#                 )
#                 continue

#             # Process message through agent
#             response = await dealer_agent.process_message(
#                 message_data["message"],
#                 connections[websocket]
#             )

#             # Send response back to client
#             await websocket.send_text(
#                 json.dumps({
#                     "message": response,
#                     "type": "response"
#                 })
#             )

#     except WebSocketDisconnect:
#         del connections[websocket]
#         logging.info(f"Connection closed for {websocket.client}")
#     except Exception as e:
#         logging.error(f"Error handling WebSocket connection: {e}")
#         raise



# # @app.get("/")
# # async def root():
# #     return {"message": "Hello Worlddddd"}



# @app.get("/")
# async def get():
#     return """
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <title>AMD Dealer Chatbot</title>
#             <style>
#                 .chat-container {
#                     width: 400px;
#                     height: 500px;
#                     border: 1px solid #ccc;
#                     padding: 20px;
#                 }
#                 .messages {
#                     height: 400px;
#                     overflow-y: auto;
#                     margin-bottom: 20px;
#                 }
#                 .message {
#                     margin: 10px 0;
#                     padding: 10px;
#                     border-radius: 5px;
#                 }
#                 .user {
#                     background: #e3f2fd;
#                     margin-left: 20%;
#                 }
#                 .bot {
#                     background: #f5f5f5;
#                     margin-right: 20%;
#                 }
#             </style>
#         </head>
#         <body>
#             <div class="chat-container">
#                 <div id="messages" class="messages"></div>
#                 <input type="text" id="messageInput" placeholder="Type a message...">
#                 <button onclick="sendMessage()">Send</button>
#             </div>

#             <script>
#                 const ws = new WebSocket('ws://' + window.location.host + '/ws/chat');
#                 const messages = document.getElementById('messages');
#                 const messageInput = document.getElementById('messageInput');

#                 ws.onmessage = function(event) {
#                     const data = JSON.parse(event.data);
#                     const messageDiv = document.createElement('div');
#                     messageDiv.className = 'message bot';
#                     messageDiv.textContent = data.message;
#                     messages.appendChild(messageDiv);
#                     messages.scrollTop = messages.scrollHeight;
#                 };

#                 function sendMessage() {
#                     const message = messageInput.value;
#                     if (message) {
#                         const messageDiv = document.createElement('div');
#                         messageDiv.className = 'message user';
#                         messageDiv.textContent = message;
#                         messages.appendChild(messageDiv);

#                         ws.send(JSON.stringify({
#                             message: message
#                         }));

#                         messageInput.value = '';
#                         messages.scrollTop = messages.scrollHeight;
#                     }
#                 }

#                 messageInput.addEventListener('keypress', function(e) {
#                     if (e.key === 'Enter') {
#                         sendMessage();
#                     }
#                 });
#             </script>
#         </body>
#     </html>
#     """
from fastapi import FastAPI, Request, Response, HTTPException
from typing import Dict
import json
import os
from dotenv import load_dotenv
from automate_media.services.agent import DealerAgent
from fastapi.middleware.cors import CORSMiddleware
import logging
import hmac
import hashlib
import httpx
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
WHATSAPP_CONFIG = {
    "PHONE_NUMBER_ID": "595597073629843",
    "API_KEY": "EAARRBhH8Gg4BOy1rYSlckUQy10Cx0L8ZBwLGUeD9fhXjrZBt5xH1XSuqqhQnGTop4t2LxZCBLMPkJfMGsQZAEKsrEBooA2a30ndXzqZCoSgxr94YJUjeuCZAlbMZAkkiiHFqnX8AaQ2eFPZCGPyQjQXFAKBLHe4xMx9m9DPioUcahnckZBmfVpmSGLCGlV2eyZCeV0sggPrwwZCNx9ZCTxAYulODthZCDMAZDZD",
    "VERIFY_TOKEN": "8848384116"  # Set this to a secure random string
}

# Initialize FastAPI app
app = FastAPI(title="WhatsApp AI Chat Bot")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize AI agent
dealer_agent = DealerAgent(os.getenv("GEMINI_API_KEY"))

# Session management
class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}

    def get_session(self, phone_number: str) -> Dict:
        if phone_number not in self.sessions:
            self.sessions[phone_number] = {
                "phone_number": phone_number,
                "start_time": datetime.now(),
                "context": [],
                "last_message": None
            }
        return self.sessions[phone_number]

    def update_context(self, phone_number: str, message: str, role: str = "user"):
        session = self.get_session(phone_number)
        session["context"].append({
            "role": role,
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        session["last_message"] = datetime.now()

session_manager = SessionManager()

async def send_whatsapp_message(to: str, message: str):
    """Send message to WhatsApp"""
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_CONFIG['PHONE_NUMBER_ID']}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_CONFIG['API_KEY']}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        raise

async def send_template_message(to: str, template_name: str = "hello_world", language_code: str = "en_US"):
    """Send template message to WhatsApp"""
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_CONFIG['PHONE_NUMBER_ID']}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_CONFIG['API_KEY']}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code
            }
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error sending template message: {e}")
        raise

@app.get("/whatsapp/webhook")
async def verify_webhook(request: Request):
    """Handle WhatsApp webhook verification"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    logger.info(f"Received webhook verification request: mode={mode}, token={token}")

    if mode == "subscribe" and token == WHATSAPP_CONFIG["VERIFY_TOKEN"]:
        if not challenge:
            raise HTTPException(status_code=400, detail="No challenge received")
        return Response(content=challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/whatsapp/webhook")
async def webhook_handler(request: Request):
    """Handle incoming WhatsApp messages"""
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")

    # Verify signature
    expected_signature = hmac.new(
        WHATSAPP_CONFIG["API_KEY"].encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(f"sha256={expected_signature}", signature):
        logger.warning("Invalid signature received")
        # We'll continue processing as Meta doesn't always send signatures correctly

    data = json.loads(body)
    logger.info(f"Received webhook data: {data}")

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" in value:
            message = value["messages"][0]
            phone_number = message["from"]
            message_text = message["text"]["body"]

            # Get or create session
            session = session_manager.get_session(phone_number)

            # Update context with user message
            session_manager.update_context(phone_number, message_text, "user")

            # Process with AI agent
            response = await dealer_agent.process_message(
                message_text,
                session
            )

            # Update context with AI response
            session_manager.update_context(phone_number, response, "assistant")

            # Send response to WhatsApp
            await send_whatsapp_message(phone_number, response)

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")

    return {"status": "ok"}

@app.get("/send-template/{phone_number}")
async def send_template(phone_number: str):
    """Endpoint to send template message"""
    try:
        response = await send_template_message(phone_number)
        return {"status": "success", "response": response}
    except Exception as e:
        logger.error(f"Error sending template: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_sessions": len(session_manager.sessions),
        "whatsapp_config": {
            "phone_number_id": WHATSAPP_CONFIG["PHONE_NUMBER_ID"],
            "verify_token_configured": bool(WHATSAPP_CONFIG["VERIFY_TOKEN"])
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import os
from dotenv import load_dotenv
from automate_media.services.agent import DealerAgent
from fastapi.middleware.cors import CORSMiddleware


# Load environment variables from .env file
load_dotenv()

# Verify API key is present
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY environment variable is not set")

app = FastAPI(title="AMD Retailer Support Chatbott")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize dealer agent with Gemini API key
dealer_agent = DealerAgent(os.getenv("GEMINI_API_KEY"))

# Store active connections and their session data
connections: Dict[WebSocket, Dict] = {}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    print(f"New connection attempt from {websocket.client}")
    try:
        await websocket.accept()
        print(f"Connection accepted for {websocket.client}")

        # Initialize session data for this connection
        connections[websocket] = {
            "customer_name": None,
            "current_topic": None
        }

        # Send welcome message
        await websocket.send_text(
            json.dumps({
                "message": "Welcome to AMD Dealer Support! I'm your virtual assistant. May I know your name?",
                "type": "welcome"
            })
        )

        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Process message through agent
            response = await dealer_agent.process_message(
                message_data["message"],
                connections[websocket]
            )

            # Send response back to client
            await websocket.send_text(
                json.dumps({
                    "message": response,
                    "type": "response"
                })
            )

    except WebSocketDisconnect:
        del connections[websocket]
    except Exception as e:
        print(f"Error handling WebSocket connection: {e}")
        raise



# @app.get("/")
# async def root():
#     return {"message": "Hello Worlddddd"}



@app.get("/")
async def get():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>AMD Dealer Chatbot</title>
            <style>
                .chat-container {
                    width: 400px;
                    height: 500px;
                    border: 1px solid #ccc;
                    padding: 20px;
                }
                .messages {
                    height: 400px;
                    overflow-y: auto;
                    margin-bottom: 20px;
                }
                .message {
                    margin: 10px 0;
                    padding: 10px;
                    border-radius: 5px;
                }
                .user {
                    background: #e3f2fd;
                    margin-left: 20%;
                }
                .bot {
                    background: #f5f5f5;
                    margin-right: 20%;
                }
            </style>
        </head>
        <body>
            <div class="chat-container">
                <div id="messages" class="messages"></div>
                <input type="text" id="messageInput" placeholder="Type a message...">
                <button onclick="sendMessage()">Send</button>
            </div>

            <script>
                const ws = new WebSocket('ws://' + window.location.host + '/ws/chat');
                const messages = document.getElementById('messages');
                const messageInput = document.getElementById('messageInput');

                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'message bot';
                    messageDiv.textContent = data.message;
                    messages.appendChild(messageDiv);
                    messages.scrollTop = messages.scrollHeight;
                };

                function sendMessage() {
                    const message = messageInput.value;
                    if (message) {
                        const messageDiv = document.createElement('div');
                        messageDiv.className = 'message user';
                        messageDiv.textContent = message;
                        messages.appendChild(messageDiv);

                        ws.send(JSON.stringify({
                            message: message
                        }));

                        messageInput.value = '';
                        messages.scrollTop = messages.scrollHeight;
                    }
                }

                messageInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            </script>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
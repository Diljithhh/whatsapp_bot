from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
import uuid

# class Lead(BaseModel):
#     id: str = Field(default_factory=lambda: str(uuid.uuid4()))
#     phone: str
#     name: Optional[str] = None
#     email: Optional[EmailStr] = None
#     product_interest: Optional[str] = None
#     conversation_history: List[str] = []
#     created_at: datetime = Field(default_factory=datetime.now)
#     status: str = "new"



# models/lead.py
class Lead(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None  # Add this line
    phone: Optional[str] = None  # Make phone optional for web users
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    product_interest: Optional[str] = None
    conversation_history: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "new"
    source: str = "web"  # Add this to distinguish between web and WhatsApp

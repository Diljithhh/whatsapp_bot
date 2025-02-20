from typing import List
from pydantic import BaseModel
from enum import Enum

class ServiceType(str, Enum):
    PURCHASE = "purchase"
    SUPPORT = "support"

class ChatMessage(BaseModel):
    message: str
    options: List[str] = []
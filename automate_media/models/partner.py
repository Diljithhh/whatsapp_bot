from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Partner(BaseModel):
    """Partner model representing registered partners/dealers."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    contactNumber: str
    contactPerson: Optional[str] = None
    partnerName: Optional[str] = None
    count: Optional[str] = "0"
    createdAt: Optional[datetime] = Field(default_factory=datetime.now)
    createdBy: Optional[str] = None
    designation: Optional[str] = None
    email: Optional[str] = None
    flange: Optional[str] = None
    floorPlan: Optional[str] = None
    gstin: Optional[str] = None
    location: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "0A8Z7EVXxINsoYZpdMt7",
                "contactNumber": "8848384116",
                "contactPerson": "Deepesh",
                "partnerName": "Vallabh IT World HPW",
                "count": "0",
                "createdAt": "2023-02-06T16:43:19",
                "createdBy": "5lPbLZldROt49dW6r2gk"
            }
        }
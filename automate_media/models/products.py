from typing import List
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str

class ProductCategory(BaseModel):
    id: int
    name: str
    description: str

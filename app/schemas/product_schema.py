from pydantic import BaseModel
from typing import Any

class Product(BaseModel):
    id: int
    name: str
    strengths: str

class BaseResponse(BaseModel):
    status: str
    data: Any

class ProductCreate(BaseModel):
    name: str
    strengths: str

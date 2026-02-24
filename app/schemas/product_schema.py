from pydantic import BaseModel
from typing import Any

class Product(BaseModel):
    id: int
    name: str
    Strengths: str

class BaseResponse(BaseModel):
    status: str
    data: Any

class ProductCreate(BaseModel):
    name: str
    Strengths: str

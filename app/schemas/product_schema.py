from pydantic import BaseModel, Field
from typing import Any

class Product(BaseModel):
    id: int
    name: str
    strengths: str

class BaseResponse(BaseModel):
    status: str
    data: Any

class ProductCreate(BaseModel):
    name: str = Field(min_length = 1, strict = True)
    strengths: str = Field(min_length = 3, strict = True)

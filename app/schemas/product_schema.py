from pydantic import BaseModel, Field, PositiveInt, field_validator
from typing import Any

class Product(BaseModel):
    id: int
    name: str
    strengths: str

class PostCartItem(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt = Field(le = 8)

class BaseResponse(BaseModel):
    status: str
    data: Any

class CartItem(BaseModel):
    cart_item_id: int
    cart_id: int
    product_id: int
    quantity: int

class ProductCreate(BaseModel):
    name: str = Field(min_length = 1, strict = True)
    strengths: str = Field(min_length = 4, strict = True)

    @field_validator("name")
    def clean_name(cls, v):
        cleaned = " ".join(v.split())
        if cleaned == "":
            raise ValueError("name cannot be empty or whitespace")
        return cleaned

    @field_validator("strengths")
    def clean_strengths(cls, v):
        cleaned = " ".join(v.split())
        if cleaned == "":
            raise ValueError("strengths cannot be empty or whitespace")
        return cleaned
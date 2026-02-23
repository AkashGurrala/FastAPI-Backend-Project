from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    Strengths: str

class ProductListResponse(BaseModel):
    status: str
    data: list[Product]
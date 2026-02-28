from typing import List
from app.schemas.product_schema import Product

def sort_products(all_products, min_id: int = None, sort_by_id: bool = False, name_contains: str = None, limit: int = None, offset: int = None) -> List[Product]:
   
    result = all_products
    
    if min_id is not None:
        result = [p for p in result if p.id >= min_id]

    if name_contains is not None:
        result = [p for p in result if name_contains.lower() in p.name.lower()]

    if sort_by_id:
        result = sorted(result, key=lambda x: x.id)
    
    if offset is not None:
        result = result[offset:]

    if limit is not None:
        result = result[:limit]
    

    return result


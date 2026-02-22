from fastapi import APIRouter, Query, Path, Request
from app.schemas.product_schema import Product
from app.services.product_service import get_filtered_products, get_singleproduct_by_id, products_count
from app.core.logger import logger

router = APIRouter()

products = [
    Product(id=1, name = 'Erwin Smith', Strengths='Leadership and Conviction'),
    Product(id=2, name = 'Gold D Roger', Strengths = 'Freedom and Strength'),
    Product(id=3, name='Asta', Strengths = 'Hardwork and Optimism'),
    Product(id=4, name = 'Monkey D Luffy', Strengths = 'Freedom and resilence'),
    Product(id=5, name = 'Gojo Satoru', Strengths = 'The Strongest'),
    Product(id=6, name = 'Tsukasa', Strengths = 'Strength and Skilled Fighter')
]

@router.get("/products/count")
def get_product_count(request: Request):

    request_id=request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching total count of products")
    count = products_count(request_id,products)

    return count

@router.get('/products/{id}', responses={ 404: {"description": "Record not found"}})
def get_product_by_id(request: Request, id: int = Path(description="The unique ID of the product to retrieve")):
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching products")
    product = get_singleproduct_by_id(request_id, products, id)
    return product

@router.get(
    "/products",
    response_model=list[Product],
    responses={
        400: {"description": "Invalid min_id"},
        404: {"description": "Record not found"},
    },
)
def get_products(
    request: Request,
    min_id: int = Query(default=None, description = "Returns records that are equal to or greater than the min id"),
    sort_by_id: bool = Query(default = False, description = "Returns records sorted in ascending order"),
    name_contains: str = Query(default = None, description = "Returns records that contain name_contains string in it"),
    limit: int = Query(default = None, description = "Return the no of records as per the limit"),
    offset: int = Query(default = None, description = "Skips the no of records based the offset vaue")
    ):
    
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching products")
    filtered = get_filtered_products(request_id, products, min_id, sort_by_id, name_contains, limit, offset)

    return filtered


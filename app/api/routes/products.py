from fastapi import APIRouter, Query, Path, Request
from app.schemas.product_schema import BaseResponse, ProductCreate
from app.services.product_service import get_filtered_products, get_singleproduct_by_id, products_count, create_product, products_search
from app.core.logger import logger

router = APIRouter()



@router.get("/products/count")
def get_product_count(request: Request):

    request_id=request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching total count of products")
    count = products_count(request_id)

    return {"status": "success",
            "data" : {"Count":  count}
            }


@router.get("/products/search", response_model = BaseResponse)
def search_products(request: Request, name: str):
    request_id = request.state.request_id
    search_list = products_search(request_id, name)
    return{"status": "Product(s) found successfully",
            "data": search_list}

@router.get(
    "/products",
    response_model=BaseResponse,
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
    filtered = get_filtered_products(request_id, min_id, sort_by_id, name_contains, limit, offset)

    return {"status": "success",
            "data": filtered}

@router.get('/products/{id}', responses={ 404: {"description": "Record not found"}})
def get_product_by_id(request: Request, id: int = Path(description="The unique ID of the product to retrieve")):
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching products")
    product = get_singleproduct_by_id(request_id, id)
    return {"status": "success",
            "data": product}

@router.post("/products", response_model=BaseResponse)
def create_new_product(request : Request, product : ProductCreate):
    request_id = request.state.request_id
    new_product=create_product(request_id, product)
    
    return {"status": "Product created successfully",
            "data": new_product}
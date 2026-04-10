from fastapi import APIRouter, Query, Path, Request
from app.schemas.product_schema import BaseResponse, PostCartItem, ProductCreate, UpdateCartItem
from app.services.product_service import update_cart_item_quantity_service, delete_cart_item_from_cart, get_cart_items, get_filtered_products, get_singleproduct_by_id, products_count, create_product, products_search, add_product_to_cart_items
from app.core.logger import logger

router = APIRouter()


@router.get("/products/count")
def get_product_count(request: Request):

    request_id=request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching total count of products")
    count = products_count(request_id)

    return {"status": "success",
            "data" : {"count":  count}}


@router.get("/products/search", response_model = BaseResponse)
def search_products(request: Request, string: str):
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching products")
    search_list = products_search(request_id, string)
    
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
    strength_contains: str = Query(default = None, description = "Return records that contain strength_contains string in it"),
    limit: int = Query(default = None, description = "Return the no of records as per the limit"),
    offset: int = Query(default = None, description = "Skips the no of records based the offset vaue")
    ):
    
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching products")
    filtered = get_filtered_products(request_id, min_id, sort_by_id, name_contains, strength_contains, limit, offset)

    return {"status": "success",
            "data": filtered}

@router.get("/cart", response_model = BaseResponse, status_code = 200)
def get_cart(request: Request):
    request_id = request.state.request_id
    user_id = 1
    logger.info(f"[{request_id}] Route: Fetching Cart Items")
    cart_items = get_cart_items(request_id, user_id)

    return {
        "status": "success",
        "data": cart_items
    }


@router.get('/products/{id}', responses={ 404: {"description": "Record not found"}})
def get_product_by_id(request: Request, id: int = Path(description="The unique ID of the product to retrieve")):
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching product")
    product = get_singleproduct_by_id(request_id, id)

    return {"status": "success",
            "data": product}

@router.post("/products", response_model=BaseResponse, status_code=201)
def create_new_product(request : Request, product : ProductCreate):
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Route: Adding product to the database")
    new_product=create_product(request_id, product)
    
    return {"status": "Product created successfully",
            "data": new_product}

@router.post("/cart/items", response_model = BaseResponse, status_code = 201)
def add_product_to_cart(request: Request, product: PostCartItem):
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Route: Adding product to the cart")
    product_added = add_product_to_cart_items(request_id, product)

    return {"status": "Product added to the cart successfully",
            "data": product_added}

@router.delete("/cart/items/{cart_item_id}", response_model = BaseResponse, status_code = 200)
def delete_cart_item(
    request: Request,
    cart_item_id: int = Path(description="The unique id of the cart item to be deleted. You can view the cart_item_id by triggering GET /cart API."),
    quantity: int | None = Query(default = None)
    ):
    request_id = request.state.request_id
    user_id = 1
    logger.info(f"[{request_id}] Route: Deleting the product from the cart")
    deletion_status = delete_cart_item_from_cart(request_id, cart_item_id, quantity, user_id)
    return {
        "status": "Product removed from the cart successfully",
        "data": deletion_status
        }

@router.patch("/cart/items/{cart_item_id}", response_model=BaseResponse)
def update_cart_item(
    request: Request,
    cart_item_id: int,
    data: UpdateCartItem
):
    request_id = request.state.request_id
    user_id = 1

    updated_item = update_cart_item_quantity_service(
        request_id, cart_item_id, data.quantity, user_id
    )

    return {
        "status": "Cart item updated successfully",
        "data": updated_item
    }
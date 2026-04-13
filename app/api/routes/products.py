from fastapi import APIRouter, Query, Path, Request
from app.schemas.product_schema import BaseResponse, PostCartItem, UpdateCartItem
from app.services.product_service import get_products, update_cart_item_quantity_service, delete_cart_item_from_cart, get_cart_items, get_singleproduct_by_id, products_count, add_product_to_cart_items
from app.core.logger import logger

router = APIRouter()


@router.get("/products/count")
def get_product_count(request: Request):

    request_id=request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching total count of products")
    count = products_count(request_id)

    return {"status": "success",
            "data" : {"count":  count}}

@router.get("/products", response_model = BaseResponse)
def get_products_route(request: Request):
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching products")
    products_list = get_products(request_id)

    return {
        "status": "success",
        "data": products_list
    }


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


@router.get('/products/{id}')
def get_product_by_id(request: Request, id: int = Path(description="The unique ID of the product to retrieve")):
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Route: Fetching product")
    product = get_singleproduct_by_id(request_id, id)

    return {"status": "success",
            "data": product}

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
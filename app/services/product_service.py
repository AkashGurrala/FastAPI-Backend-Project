from app.core.logger import logger
from app.data.store import get_all_products, update_quantity_in_cart, delete_all_cart_item_cart, get_quantity_from_cart_items, get_cart_items_with_product, increase_product_quantity, get_quantity_from_cart, add_product_to_cart, get_cart_id, create_cart, get_product_id_availability, get_user, product_by_id, count_products
from app.services.exceptions import BadRequestException, NoProductFoundException, ProductUnavailableException, UserDoesNotExistException


def get_products(request_id):
    logger.info(f"[{request_id}] Service: called with GET /products")
    product_list = get_all_products(request_id)
    if product_list is None:
        logger.info(f"[{request_id}] Service: Product page is empty")
    
    return product_list or []

def get_singleproduct_by_id(request_id, id):

    logger.info(f"[{request_id}] Service: called with id={id}")


    if id is not None and id < 1:
        logger.warning(f"[{request_id}] id should be equal to or greater than one.")
        raise BadRequestException("Invalid id recieved. id should be equal to or greater than one.")

    result = product_by_id(request_id, id)
    if result is None:
        raise NoProductFoundException("No product found")
    
    return result

def products_count(request_id):
    count = count_products(request_id)
    logger.info(f"[{request_id}] Service: called for count of products")
    logger.info(f"[{request_id}] Count: {count}")
    return count


def add_product_to_cart_items(request_id, product):
    user_id = 1
    product_id = product.product_id
    quantity = product.quantity

    verify_user = get_user(request_id, user_id)
    if verify_user == None:
        raise UserDoesNotExistException("given user_id does not exist")
    
    cart_id = get_cart_id(request_id, user_id)
    if cart_id == None:
        cart_id = create_cart(request_id, user_id)

    verify_product = get_product_id_availability(request_id, product_id)
    if verify_product is None:
        raise NoProductFoundException("product_id does not exist")
    
    if not verify_product["is_available"]:
        raise ProductUnavailableException("product exists but currently unavailable")

    if quantity <= 0 or quantity > 8:
        raise BadRequestException("quanitity is out of range. quantity should be greater than 0 and less than 8.")

    logger.info(f"[{request_id}] Service: Input Verfication Successful. Proceeding with next steps")

    product_quantity = get_quantity_from_cart(request_id, cart_id, product_id)

    if product_quantity is None:
        cart_item = add_product_to_cart(request_id, cart_id, product_id, quantity)
    else:
        new_quantity = product_quantity + quantity
        if new_quantity <= 0 or new_quantity > 8:
            raise BadRequestException("quanitity is out of range. quantity should be greater than 0 and less than 8.")
        cart_item = increase_product_quantity(request_id, cart_id, product_id, new_quantity)

    logger.info(f"[{request_id}] Service: Product is successully added to the cart")

    return cart_item


def get_cart_items(request_id, user_id):
    verify_user = get_user(request_id, user_id)
    
    if verify_user == None:
        raise UserDoesNotExistException("given user_id does not exist")
    
    cart_id = get_cart_id(request_id, user_id)
    if cart_id == None:
        cart_id = create_cart(request_id, user_id)
    
    cart_items = get_cart_items_with_product(request_id, cart_id)

    cart_total_price = 0
    final_result = []

    for item in cart_items:
        item_total_price = item["price"] * item["quantity"]
        cart_total_price += item_total_price

        final_result.append({
            "cart_item_id": item["cart_item_id"],
            "product_id": item["product_id"],
            "product_name": item["product_name"],
            "price": item["price"],
            "quantity": item["quantity"],
            "item_total_price": item_total_price 
        })

    return {
        "cart_id": cart_id,
        "cart_items": final_result,
        "cart_total_price" : cart_total_price
    }

def delete_cart_item_from_cart(request_id, cart_item_id, quantity, user_id):
    verify_user = get_user(request_id, user_id)
    if verify_user == None:
        raise UserDoesNotExistException("given user_id does not exist")
    
    cart_id = get_cart_id(request_id, user_id)
    if cart_id == None:
        raise NoProductFoundException("The cart is empty")
    
    get_quantity = get_quantity_from_cart_items(request_id, cart_id, cart_item_id)

    if get_quantity is None:
        raise NoProductFoundException(f"Item with id={cart_item_id} is not found in the cart.")

    if quantity is not None and quantity > get_quantity:
        raise BadRequestException("Cannot delete more than existing quantity")
    
    

    if quantity is None:
        result = delete_all_cart_item_cart(request_id, cart_item_id, cart_id)
    else:
        new_quantity = get_quantity - quantity
        if new_quantity == 0:
            result = delete_all_cart_item_cart(request_id, cart_item_id, cart_id)
        else:
            result = update_quantity_in_cart(request_id, cart_item_id, cart_id, new_quantity)
    
    if result:
        result = "deletion successful"
    else:
        result = "deletion failed"

    return {
        "deletion status": result
    }


def update_cart_item_quantity_service(request_id, cart_item_id, quantity, user_id):

    # 1. validate user
    user = get_user(request_id, user_id)
    if user is None:
        raise UserDoesNotExistException("User does not exist")

    # 2. get cart
    cart_id = get_cart_id(request_id, user_id)
    if cart_id is None:
        raise NoProductFoundException("Cart is empty")

    # 3. check item exists
    existing_quantity = get_quantity_from_cart_items(request_id, cart_id, cart_item_id)

    if existing_quantity is None:
        raise NoProductFoundException("Cart item not found")

    # 4. update quantity
    updated_item = update_quantity_in_cart(request_id, cart_item_id, cart_id, quantity)

    return updated_item
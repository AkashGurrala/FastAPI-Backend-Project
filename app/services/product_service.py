from app.core.logger import logger
from app.data.store import update_quantity_in_cart, delete_all_cart_item_cart, get_quantity_from_cart_items, get_cart_items_with_product, increase_product_quantity, get_quantity_from_cart, add_product_to_cart, get_cart_id, create_cart, get_product_id_availability, get_user, product_by_id, count_products, add_product, search_products, get_products
from app.services.exceptions import BadRequestException, InvalidInputException, NoProductFoundException, ProductUnavailableException, UserDoesNotExistException

def get_singleproduct_by_id(request_id, id):

    logger.info(f"[{request_id}] Service: called with id={id}")


    if id is not None and id < 1:
        logger.warning(f"[{request_id}] id should be equal to or greater than one.")
        raise BadRequestException("Invalid id recieved. id should be equal to or greater than one.")

    result = product_by_id(request_id, id)
    if result is None:
        raise NoProductFoundException("No product found")
    
    return result

def get_filtered_products(request_id, min_id, sort_by_id, name_contains, strength_contains, limit, offset):

    logger.info(f"[{request_id}] Service: called with min_id={min_id}, sort_by_id={sort_by_id}, name_contains={name_contains}, streng limit={limit}, offset={offset}")

    if min_id is not None and min_id < 1:
        logger.warning(f"[{request_id}] Invalid min_id value received")
        raise BadRequestException("Invalid min_id. Please try again with the approriate min_id value.")
    
    if limit is not None and limit < 1:
        logger.warning(f"[{request_id}] Invalid Limit value recieved")
        raise BadRequestException("Invalid limit value recieved. Limit value must be equal to or greater than 1")
    
    if limit is not None and limit > 100:
        logger.warning(f"[{request_id}] Limit value exceeds maximum allowed (100)")
        raise BadRequestException("Limit value exceeds 100. Limit value must be less than or equal to 100.")

    if offset is not None and offset < 0:
        logger.warning(f"[{request_id}] Invalid offset value recieved")
        raise BadRequestException("Invalid offset value recieved. Offset value must be equal to or greater than 0")

    if name_contains:   
        name_contains = " ".join(name_contains.split())
    
    if strength_contains:
        strength_contains = " ".join(strength_contains.split())

    filtered = get_products(request_id, min_id, sort_by_id, name_contains, strength_contains, limit, offset)

    logger.info(f"[{request_id}] Service: Returning {len(filtered)} products")
    return filtered

def products_count(request_id):
    count = count_products(request_id)
    logger.info(f"[{request_id}] Service: called for count of products")
    logger.info(f"[{request_id}] Count: {count}")
    return count

def create_product(request_id, product):
    
    logger.info(f"[{request_id}] Service: Adding new product ")
    product = add_product(request_id, product)
    return product

def products_search(request_id, string):
    string = " ".join(string.split())
    logger.info(f"[{request_id}] Service: Called for searching all products that include '{string}' in the row values")

    if string == "":
        raise InvalidInputException(
            "Empty spaces or no input are considered Invalid. Please provide appropriate input."
            )

    search_list = search_products(request_id, string)

    if not search_list:
        logger.info(f"[{request_id}] Service: No product returned with string {string} in the row values")
    
    logger.info(f"[{request_id}] Service: Returning {len(search_list)} products")

    return search_list

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
    print(verify_product)
    if verify_product is None:
        raise NoProductFoundException("product_id does not exist")
    
    if not verify_product["is_available"]:
        raise ProductUnavailableException("product exists but currently unavailable")

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
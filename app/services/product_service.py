from app.api.routes import products
from app.logic import sort_products
from app.core.logger import logger
from app.schemas.product_schema import Product
from app.data.store import products

class NoProductFoundException(Exception):
    pass

class InvalidInputException(Exception):
    pass


def get_singleproduct_by_id(request_id, id):

    logger.info(f"[{request_id}] Service called with id={id}")


    if id is not None and id < 1:
        logger.warning('id should be equal to or greater than one.')
        raise InvalidInputException("Invalid id recieved. id should be equal to or greater than one.")

    for product in products:
        if product.id==id:
            return product

    raise NoProductFoundException("No product found")

def get_filtered_products(request_id, min_id, sort_by_id, name_contains, limit, offset):

    logger.info(f"[{request_id}] Service called with min_id={min_id}, sort_by_id={sort_by_id}, name_contains={name_contains}, limit={limit}, offset={offset}")

    if min_id is not None and min_id < 1:
        logger.warning("Invalid min_id value received")
        raise InvalidInputException("Invalid min_id. Please try again with the approriate min_id value.")
    
    if limit is not None and limit < 1:
        logger.warning("Invalid Limit value recieved")
        raise InvalidInputException("Invalid limit value recieved. Limit value must be equal to or greater than 1")

    if offset is not None and offset < 0:
        logger.warning("Invalid offset value recieved")
        raise InvalidInputException("Invalid offset value recieved. Offset value must be equal to or greater than 0")

    filtered = sort_products(products, min_id, sort_by_id, name_contains, limit, offset)

    if not filtered:
        logger.warning("No products found after filtering.")
        raise NoProductFoundException("Product not found.")
    
    logger.info(f"[{request_id}] {len(filtered)} products returned")
    return filtered

def products_count(request_id):
    count = len(products)
    logger.info(f"[{request_id}] Count: {count}")
    return {"count": count}

def create_product(request_id, product):
    
    logger.info(f"[{request_id}] Adding new product")
    product_list = products

    if not product_list:
        new_id = 1
    else:
        new_id= max(p.id for p in product_list) + 1

    new_product = Product(
        id = new_id,
        name = product.name,
        strengths = product.strengths)
    
    for p in products:
        if p.name.lower() == new_product.name.lower():
            raise InvalidInputException("Product name already exists")

    products.append(new_product)
    logger.info(f"[{request_id}] Product is created with id = {new_id}")
    return new_product


def products_search(request_id, name):
    logger.info(f"[{request_id}] Searching all products that include '{name}' in the name")

    search_list= []
    for p in products:
        if name.lower() in p.name.lower():
            search_list.append(p)
    
    if not search_list:
        raise NoProductFoundException(f"No product found with name: {name}")
    
    return search_list
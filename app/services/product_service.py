from app.logic import sort_products
from app.core.logger import logger
from app.data.store import get_all_products, product_by_id, count_products, add_product, search_products
from app.services.exceptions import InvalidInputException, NoProductFoundException

def get_singleproduct_by_id(request_id, id):

    logger.info(f"[{request_id}] Service called with id={id}")


    if id is not None and id < 1:
        logger.warning('id should be equal to or greater than one.')
        raise InvalidInputException("Invalid id recieved. id should be equal to or greater than one.")

    result = product_by_id(request_id, id)
    if not result:
        raise NoProductFoundException("No product found")
    
    return result

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

    all_products = get_all_products(request_id)

    filtered = sort_products(all_products, min_id, sort_by_id, name_contains, limit, offset)

    logger.info(f"[{request_id}] {len(filtered)} products returned")
    return filtered

def products_count(request_id):
    count = count_products()
    if count is None:
        count = 0
    logger.info(f"[{request_id}] Count: {count}")
    return {"count": count}

def create_product(request_id, product):
    
    logger.info(f"[{request_id}] Adding new product")
    product.name = " ".join(product.name.split())
    product.strengths = " ".join(product.strengths.split())
    product = add_product(request_id, product)
    return product


def products_search(request_id, name):
    name = name.strip()
    logger.info(f"[{request_id}] Searching all products that include '{name}' in the name")

    if name == "":
        raise InvalidInputException(
            "Empty spaces or no input are considered Invalid. Please provide appropriate input."
            )

    search_list = search_products(request_id, name)

    if not search_list:
        logger.info(f"No product found with name: {name}")
    
    return search_list

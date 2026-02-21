from operator import countOf
from app.logic import sort_products
from app.core.logger import logger

class InvalidIdException(Exception):
    pass

class NoProductFoundException(Exception):
    pass


def get_singleproduct_by_id(request_id, products, id):

    logger.info(f"[{request_id}] Service called with id={id}")


    if id is not None and id < 1:
        logger.warning('id should be equal to or greater than one.')
        raise InvalidIdException("Invalid id recieved. id should be equal to or greater than one.")

    for product in products:
        if product.id==id:
            return product

    raise NoProductFoundException("No product found")

def get_filtered_products(request_id, products, min_id, sort_by_id, name_contains, limit, offset):

    logger.info(f"[{request_id}] Service called with min_id={min_id}, sort_by_id={sort_by_id}, name_contains={name_contains}, limit={limit}, offset={offset}")

    if min_id is not None and min_id < 1:
        logger.warning("Invalid min_id value received")
        raise InvalidIdException("Invalid min_id. Please try again with the approriate min_id value.")
    
    filtered = sort_products(products, min_id, sort_by_id, name_contains, limit, offset)

    if not filtered:
        logger.warning("No products found after filtering.")
        raise NoProductFoundException("Product not found.")
    
    logger.info(f"[{request_id}] {len(filtered)} products returned")
    return filtered

def products_count(request_id,products):
    count = len(products)
    return {"count": count}
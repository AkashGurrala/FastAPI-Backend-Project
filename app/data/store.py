from app.schemas.product_schema import Product
from app.services.exceptions import InvalidInputException
from app.core.logger import logger

products = [
    Product(id=1, name = 'Erwin Smith', strengths='Leadership and Conviction'),
    Product(id=2, name = 'Gold D Roger', strengths = 'Freedom and Strength'),
    Product(id=3, name='Asta', strengths = 'Hardwork and Optimism'),
    Product(id=4, name = 'Monkey D Luffy', strengths = 'Freedom and resilence'),
    Product(id=5, name = 'Gojo Satoru', strengths = 'The Strongest'),
    Product(id=6, name = 'Tsukasa', strengths = 'Strength and Skilled Fighter')
]

def get_all_products():
    return products


def product_by_id(id: int):
    
    product = [p for p in products if p.id == id]
    return product

def count_products():
    count = len(products)
    return count

def add_product(request_id, product):
    
    new_id=len(products)+1
    new_product = Product(
        id = new_id,
        name = product.name,
        strengths= product.strengths
    )
    
    products.append(new_product)
    logger.info(f"[{request_id}] Product is successfully added to the database")

    return new_product

def search_products(name: str):
    
    search_list=[]
    for p in products:
        if name in p.name:
            search_list.append(p)

    return search_list
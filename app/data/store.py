import psycopg2
from app.schemas.product_schema import Product, CartItem
from app.core.logger import logger
from app.db.connection import get_db_connection
from app.services.exceptions import DatabaseOperationException, DuplicateProductException
from typing import List


def raw_info_to_product(row):
    return Product(id = row[0], name = row[1], strengths = row[2])

def cart_item_schema(row):
    return CartItem(cart_item_id = row[0], cart_id = row[1], product_id = row[2], quantity = row[3])


def product_by_id(request_id, id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM products where id=%s;', (id,))
                result=cursor.fetchone()
                if result is not None:
                    result = raw_info_to_product(result)
                logger.info(f"[{request_id}] Store: Database Fetch Successful:")
                return result
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")


def count_products(request_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT COUNT (*) FROM products;')
                result=cursor.fetchone()[0]
                logger.info(f"[{request_id}] Store: Database Fetch Successful:")
                return result
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")


def add_product(request_id, product):

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO products (name, strengths) values (%s,%s) RETURNING id, name, strengths;",(product.name, product.strengths))
                result = cursor.fetchone()
                result = raw_info_to_product(result)
                logger.info(f"[{request_id}] Store: Database Insert Successful")
                return result
    
    except psycopg2.IntegrityError as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DuplicateProductException(f"Product name: '{product.name}' already exists.")

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")

def get_user(request_id, user_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id FROM users WHERE user_id = %s;",(user_id,))
                result = cursor.fetchone()
                logger.info(f"[{request_id}] Store: Database Fetch Successful")
                return result[0] if result else None
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")     
                
def get_product_id_availability(request_id, product_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT product_id, is_available FROM all_products WHERE product_id = %s;",(product_id,))
                result = cursor.fetchone()
                logger.info(f"[{request_id}] Store: Database Fetch Successful")
                if result is None:
                    return None
                db_product_id, is_available = result
                return {
                    "product_id": db_product_id,
                    "is_available": is_available
                }

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed") 

def get_cart_id(request_id, user_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT cart_id FROM carts WHERE user_id = %s;",(user_id,))
                result = cursor.fetchone()
                logger.info(f"[{request_id}] Store: Database Fetch Successful")
                return result[0] if result else None

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")

def create_cart(request_id, user_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO carts (user_id) values (%s) RETURNING cart_id;",(user_id,))
                result = cursor.fetchone()
                logger.info(f"[{request_id}] Store: Database Insert Successful")
                return result[0] if result else None

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")      

def get_quantity_from_cart(request_id, cart_id, product_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT quantity FROM cart_items WHERE cart_id = %s AND product_id = %s",(cart_id, product_id))
                result = cursor.fetchone()
                return result[0] if result else None
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed") 

def increase_product_quantity(request_id, cart_id, product_id, quantity):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE cart_items set quantity = %s where cart_id = %s AND product_id = %s RETURNING cart_item_id, cart_id, product_id, quantity;",(quantity, cart_id, product_id))
                raw_result = cursor.fetchone()
                result = cart_item_schema(raw_result)
                logger.info(f"[{request_id}] Store: Database Fetch Successful")
                return result    
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")    

def add_product_to_cart(request_id, cart_id, product_id, quantity):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO cart_items (cart_id, product_id, quantity) values (%s, %s, %s) RETURNING cart_item_id, cart_id, product_id, quantity;",(cart_id, product_id, quantity))
                raw_result = cursor.fetchone()
                result = cart_item_schema(raw_result)
                logger.info(f"[{request_id}] Store: Database Fetch Successful")
                return result    
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed") 

def get_cart_items_with_product(request_id, cart_id):
     try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT
                    ci.cart_item_id,
                    ci.product_id,
                    ci.quantity,
                    p.product_name,
                    p.price
                FROM cart_items ci
                JOIN all_products p
                    on ci.product_id = p.product_id
                WHERE ci.cart_id = %s;
                    """
                cursor.execute(query, (cart_id,))
                raw_result = cursor.fetchall()
                result = []
                for item in raw_result:
                    x = {
                        "cart_item_id": item[0],
                        "product_id": item[1],
                        "quantity": item[2],
                        "product_name": item[3],
                        "price": item[4]
                        }
                    result.append(x)
                
                return result

     except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")        


def search_products(request_id, string: str):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM products WHERE name ILIKE %s OR strengths ILIKE %s ;", (f"%{string}%", f"%{string}%"))
                product_list=cursor.fetchall()
                logger.info(f"[{request_id}] Store: Database Fetch Successful:")
                result = [raw_info_to_product(row) for row in product_list]
                return result
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")


def get_products(
    request_id, 
    min_id: int = None, 
    sort_by_id: bool = False, 
    name_contains: str = None, 
    strength_contains: str = None,
    limit: int = None, 
    offset: int = None) -> List[Product]:

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT id, name, strengths FROM products WHERE 1=1"
                params = []

                if min_id is not None:
                    query += " AND id >= %s"
                    params.append(min_id)

                if name_contains:
                    query += " AND name ilike %s"
                    params.append(f"%{name_contains}%")
                
                if strength_contains:
                    query += " AND strengths ilike %s"
                    params.append(f"%{strength_contains}%")
                
                if sort_by_id:
                    query += " ORDER BY id"

                if limit is not None:
                    query += " LIMIT %s"
                    params.append(limit)

                if offset is not None:
                    query += " OFFSET %s"
                    params.append(offset)

                cursor.execute(query, params)
                product_list = cursor.fetchall()
                logger.info(f"[{request_id}] Store: Database Fetch Successful")
                result = [raw_info_to_product(row) for row in product_list]
                return result

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")

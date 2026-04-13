import psycopg2
from app.schemas.product_schema import CartItem, ProductItem
from app.core.logger import logger
from app.db.connection import get_db_connection
from app.services.exceptions import DatabaseOperationException

def cart_item_schema(row):
    return CartItem(cart_item_id = row[0], cart_id = row[1], product_id = row[2], quantity = row[3])

def product_item_schema(row):
    return ProductItem(product_id = row[0], product_name = row[1], category = row[2], price = row[3])

def get_all_products(request_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT product_id, product_name, category, price FROM all_products where is_available=true;') 
                raw_result = cursor.fetchall()
                if raw_result is not None:
                    result = []
                    for row in raw_result:
                        x = {
                        "product_id": raw_result[0],
                        "product_name": raw_result[1],
                        "category": raw_result[2],
                        "price": raw_result[3]
                        }
                        result.append(x)
                logger.info(f"[{request_id}] Store: Database Fetch Successful:")
                return result

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")

def product_by_id(request_id, id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT product_id, product_name, category, price FROM all_products where is_available=true and product_id=%s;",(id,))
                raw_result = cursor.fetchone()

                if raw_result is None:
                    return None

                result = {
                "product_id": raw_result[0],
                "product_name": raw_result[1],
                "category": raw_result[2],
                "price": raw_result[3]
                }
                logger.info(f"[{request_id}] Store: Database Fetch Successful:")
                return result

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")


def count_products(request_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT COUNT (*) FROM all_products;')
                result=cursor.fetchone()[0]
                logger.info(f"[{request_id}] Store: Database Fetch Successful:")
                return result
    
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


def get_quantity_from_cart_items(request_id, cart_id, cart_item_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT quantity FROM cart_items WHERE cart_id = %s AND cart_item_id = %s", (cart_id, cart_item_id))
                result = cursor.fetchone()
                logger.info(f"[{request_id}] Store: Database Fetch Successful")
                return result[0] if result else None
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operartion Failed")


def delete_all_cart_item_cart(request_id, cart_item_id, cart_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cart_items where cart_id = %s and cart_item_id = %s", (cart_id, cart_item_id))
                logger.info(f"[{request_id}] Store: Database Deletion Successful")
                return True
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operartion Failed")   
                     
def update_quantity_in_cart(request_id, cart_item_id, cart_id, quantity):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE cart_items
                    SET quantity = %s
                    WHERE cart_id = %s AND cart_item_id = %s
                    RETURNING cart_item_id, cart_id, product_id, quantity;
                """, (quantity, cart_id, cart_item_id ))

                result = cursor.fetchone()
                return cart_item_schema(result)
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Store: Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operartion Failed")

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
                WHERE ci.cart_id = %s
                AND p.is_available = true;
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
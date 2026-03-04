import psycopg2
from app.schemas.product_schema import Product
from app.core.logger import logger
from app.db.connection import get_db_connection
from app.services.exceptions import DatabaseOperationException, DuplicateProductException

# Current: In-memory store (temporary)
# Next: Will be replaced by postgreSQL queries

def raw_info_to_product(row):
    return Product(id = row[0], name = row[1], strengths = row[2])

def get_all_products(request_id):
    try:
        conn = None
        cursor = None
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products;')
        product_list = cursor.fetchall()
        result = []
        for row in product_list:
            product = raw_info_to_product(row)
            result.append(product)
        logger.info("Database operation successfull")
        return result

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def product_by_id(request_id, id: int):
    try:
        conn = None
        cursor = None
        conn=get_db_connection()
        cursor=conn.cursor()

        cursor.execute('SELECT * FROM products where id=%s;', (id,))
        result=cursor.fetchone()
        if result is not None:
            result = raw_info_to_product(result)
        logger.info("Database operation successful:")
        return result
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
'''
def product_by_name(name):
    try:
        conn = None
        cursor = None
        conn=get_db_connection()
        cursor=conn.cursor()

        cursor.execute('SELECT * FROM products where name ilike %s;', (name,))
        result = cursor.fetchone()
        return result
    
    except Exception as e:
        logger.info("Database Operation Failed:", str(e))
        raise
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
'''
def count_products(request_id):
    try:
        conn = None
        cursor = None
        conn=get_db_connection()
        cursor=conn.cursor()

        cursor.execute('SELECT COUNT (*) FROM products;')
        result=cursor.fetchone()[0]
        logger.info("Database operation successful:")
        return result
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def add_product(request_id, product):

    try:
        conn = None
        cursor = None
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO products (name, strengths) values (%s,%s) RETURNING id, name, strengths;",(product.name, product.strengths))
        conn.commit()
        result = cursor.fetchone()
        result = raw_info_to_product(result)
        logger.info("Database operation successful:")
        return result
    
    except psycopg2.IntegrityError as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DuplicateProductException(f"Product name: '{product.name}' already exists.")

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def search_products(request_id, name: str):
    try:
        conn = None
        cursor = None
        conn=get_db_connection()
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM products where name ilike %s;", (f"%{name}%",))
        product_list=cursor.fetchall()
        logger.info("Database fetch successful:")
        result=[]
        if product_list is not None:
            for row in product_list:
                product = raw_info_to_product(row)
                result.append(product)
        return result
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
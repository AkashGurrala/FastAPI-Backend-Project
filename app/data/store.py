from itertools import product
from unittest import result
from app.schemas.product_schema import Product
from app.core.logger import logger
from app.db.connection import get_db_connection

# Current: In-memory store (temporary)
# Next: Will be replaced by postgreSQL queries


def get_all_products():
    try:
        conn = None
        cursor = None
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products;')
        rows = cursor.fetchall()
        result = []
        for row in rows:
            product = Product(
                id= row[0],
                name= row[1],
                strengths= row[2]
            )
            result.append(product)
        print("Database Fetch Successful")
        return result
    
    except Exception as e:
        print("Database operation failed: ", str(e))
        print("Since DB operation is failed, using in-memory list to commplete operation")
        return products
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def product_by_id(id: int):
    try:
        conn = None
        cursor = None
        conn=get_db_connection()
        cursor=conn.cursor()

        cursor.execute('SELECT * FROM products where id=%s;', (id,))
        result=cursor.fetchall()
        print("Database operation successful:")
        return result
    
    except Exception as e:
        print("Database Operation Failed:", str(e))
        return []
    
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
        print("Database Operation Failed:", str(e))
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
'''
def count_products():
    try:
        conn = None
        cursor = None
        conn=get_db_connection()
        cursor=conn.cursor()

        cursor.execute('SELECT COUNT (*) FROM products;')
        result=cursor.fetchone()[0]
        logger.info("Database operation successful:")
        return result
    
    except Exception as e:
        logger.error("Database Operation Failed:", str(e))
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def add_product(product):

    try:
        conn = None
        cursor = None
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO products (name, strengths) values (%s,%s);",(product.name, product.strenghts))
        conn.commit()
        cursor.execute("SELECT * FROM products WHERE name = %s", (product.name,))
        result = cursor.fetchone()
        result = Product(
            id = result[0],
            name = result[1],
            strengths = result[2] 
        )
        print("Database operation successful:")
        return result
    
    except Exception as e:
        print("Database Operation Failed:", str(e))
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def search_products(name: str):
    try:
        conn = None
        cursor = None
        conn=get_db_connection()
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM products where name ilike %s;", (f"%{name}%",))
        product_list=cursor.fetchall()
        print("Database fetch successful:")
        result=[]
        for row in product_list:
            product = Product(
                id = row[0],
                name = row[1],
                strengths = row[2]
            )
            result.append(product)

        return result
    
    except Exception as e:
        print("Database Operation Failed:", str(e))
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
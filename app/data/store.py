import psycopg2
from app.schemas.product_schema import Product
from app.core.logger import logger
from app.db.connection import get_db_connection
from app.services.exceptions import DatabaseOperationException, DuplicateProductException
from typing import List

# Current: In-memory store (temporary)
# Next: Will be replaced by postgreSQL queries

def raw_info_to_product(row):
    return Product(id = row[0], name = row[1], strengths = row[2])


def product_by_id(request_id, id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM products where id=%s;', (id,))
                result=cursor.fetchone()
                if result is not None:
                    result = raw_info_to_product(result)
                logger.info(f"[{request_id}] Database fetch successful:")
                return result
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")


def count_products(request_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT COUNT (*) FROM products;')
                result=cursor.fetchone()[0]
                logger.info(f"[{request_id}] Database operation successful:")
                return result
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")


def add_product(request_id, product):

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO products (name, strengths) values (%s,%s) RETURNING id, name, strengths;",(product.name, product.strengths))
                result = cursor.fetchone()
                result = raw_info_to_product(result)
                logger.info(f"[{request_id}] Database operation successful:")
                return result
    
    except psycopg2.IntegrityError as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DuplicateProductException(f"Product name: '{product.name}' already exists.")

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")


def search_products(request_id, name: str):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM products WHERE name ILIKE %s OR strengths ILIKE %s ;", (f"%{name}%", f"%{name}%"))
                product_list=cursor.fetchall()
                logger.info(f"[{request_id}] Database fetch successful:")
                result = [raw_info_to_product(row) for row in product_list]
                return result
    
    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
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
                logger.info(f"[{request_id}] Database fetch successful")
                result = [raw_info_to_product(row) for row in product_list]
                return result

    except psycopg2.Error as e:
        logger.error(f"[{request_id}] Database Operation Failed: {e}")
        raise DatabaseOperationException("Database Operation Failed")

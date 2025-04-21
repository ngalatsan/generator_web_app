import psycopg2
from contextlib import contextmanager
from config import config

DB_CONFIG = {
    "dbname": config['DB_NAME'],
    "user": config['DB_USER'],
    "password": config['DB_PASSWORD'],
    "host": config['DB_HOST']
}

@contextmanager
def get_db_connection():
    """Контекстный менеджер для подключения к БД"""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_db_cursor():
    """Контекстный менеджер для курсора"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except:
            conn.rollback()
            raise

def save_password(password, length, use_uppercase, use_digits, use_special):
    query = """
    INSERT INTO generated_passwords 
    (password, length, use_uppercase, use_digits, use_special)
    VALUES (%s, %s, %s, %s, %s)
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, (password, length, use_uppercase, use_digits, use_special))

def save_uuid(uuid_value):
    query = """
    INSERT INTO generated_uuids 
    (uuid)
    VALUES (%s)
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, (uuid_value,))

def save_coordinates(latitude, longitude):
    query = """
    INSERT INTO generated_coordinates 
    (latitude, longitude)
    VALUES (%s, %s)
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, (latitude, longitude))

def save_color(hex_code, red, green, blue):
    query = """
    INSERT INTO generated_colors 
    (hex_code, red, green, blue)
    VALUES (%s, %s, %s, %s)
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, (hex_code, red, green, blue))
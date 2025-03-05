import mysql.connector  # Ensure mysql.connector is imported
from dotenv import load_dotenv
from contextlib import contextmanager
import os

load_dotenv()

# Consolidated DB connection function
def get_db_connection(db_type="discord", timeout=5):
    if db_type == "discord":
        return mysql.connector.connect(
            host=os.getenv("DISCORD_DB_HOST"),
            user=os.getenv("DISCORD_DB_USER"),
            password=os.getenv("DISCORD_DB_PASSWORD"),
            database=os.getenv("DISCORD_DB_NAME"),
            connection_timeout=timeout
        )
    elif db_type == "wishlist":
        return mysql.connector.connect(
            host=os.getenv("WISHLIST_DB_HOST"),
            user=os.getenv("WISHLIST_DB_USER"),
            password=os.getenv("WISHLIST_DB_PASSWORD"),
            database=os.getenv("WISHLIST_DB_NAME"),
            connection_timeout=timeout
        )
    elif db_type == "api":
        return mysql.connector.connect(
            host=os.getenv("API_DB_HOST"),
            user=os.getenv("API_DB_USER"),
            password=os.getenv("API_DB_PASSWORD"),
            database=os.getenv("API_DB_NAME"),
            connection_timeout=timeout
        )

@contextmanager
def db_connection(db_type="discord"):
    conn = None
    try:
        conn = get_db_connection(db_type)
        yield conn
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        raise
    finally:
        if conn is not None:
            conn.close()

# Helper function to execute queries
def execute_query(db_type, query, params=None, fetchall=True, commit=False):
    try:
        with db_connection(db_type) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                if commit:
                    conn.commit()
                if fetchall:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
        return result
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        raise  # Rethrow the exception so it can be handled by the calling function
    
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise  # Rethrow any other unexpected exceptions
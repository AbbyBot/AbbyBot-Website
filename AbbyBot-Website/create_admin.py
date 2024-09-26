import mysql.connector
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash

# Load dotenv variables
load_dotenv()

# DB Connect
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("WISHLIST_DB_HOST"),
        user=os.getenv("WISHLIST_DB_USER"),
        password=os.getenv("WISHLIST_DB_PASSWORD"),
        database=os.getenv("WISHLIST_DB_NAME")
    )

# Create admin
def create_admin(username, email, password):
    password_hash = generate_password_hash(password)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new admin
        cursor.execute("""
            INSERT INTO admins (username, email, password) 
            VALUES (%s, %s, %s)
        """, (username, email, password_hash))
        
        conn.commit()
        print("Manager created successfully.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        cursor.close()
        conn.close()

# Request the information of the new administrator
if __name__ == "__main__":
    username = input("Enter the username: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    # Create admin
    create_admin(username, email, password)

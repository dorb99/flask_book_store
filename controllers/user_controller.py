import sqlite3
import logging
import os
from flask import abort, request
from config.db import get_db_conn 


# logger = setup_logger()

# get user
def get_user(id):
    try:    
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        found_user = cursor.fetchone()
        conn.close()
        endpoint = request.endpoint
        logging.info(f"{endpoint}: {found_user}")
        return found_user
    except Exception as e:
        logging.error(str(e))
        abort(500)
    
# get all users
def get_all_users():
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        logging.info(f"Looked and found users: {len(users)}")
        return users
    except Exception as e:
        logging.error(str(e))
        abort(500)
        
# create user
def create_user(user):
    """
    - receive a user as a tuple of (username, password, email, age)
    """
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, password, email, age)
            VALUES (?, ?, ?, ?)
        """, user
        )
        conn.commit()
        
        user_id = cursor.lastrowid
        logging.info(f"Created a user with a user_id of: {user_id}")
        conn.close()
        return {"message": "Created user", "id": user_id}
    except Exception as e:
        logging.error(str(e))
        abort(500)

def get_user_by_username(username):
    try:    
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        found_user = cursor.fetchone()
        conn.close()
        endpoint = request.endpoint
        return found_user
    except Exception as e:
        logging.error(str(e))
        abort(500)

# update user
# delete user

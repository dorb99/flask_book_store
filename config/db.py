import sqlite3
import os
from dotenv import load_dotenv

# os.makedirs("databases/tmp", exist_ok=True)
global db_path

def init_db():
    global db_path
    load_dotenv()
    DATABASE_NAME = os.getenv("DATABASE_NAME", "app.db")
    tmp_path = os.path.join("config", "tmp")
    
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
        
    db_path = os.path.join(tmp_path, DATABASE_NAME)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS users(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username      UNIQUE NOT NULL,
                           password TEXT NOT NULL,
                           email TEXT NOT NULL,
                           age INTEGER NOT NULL
                       );
                       """)
        conn.commit()
        print("Connected and created tables")
    

def get_db_conn():
    return sqlite3.connect(db_path)
    
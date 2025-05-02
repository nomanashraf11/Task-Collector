import sqlite3
from sqlite3 import Error
import os

def create_connection():
    conn = None
    try:
   
        if not os.path.exists('data'):
            os.makedirs('data')
        
        conn = sqlite3.connect('data/task_manager.db')
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
    
    return conn

def initialize_database():
    conn = create_connection()
    
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    is_admin INTEGER DEFAULT 0
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority INTEGER DEFAULT 2,  -- 1: High, 2: Medium, 3: Low
                    due_date TEXT,
                    status TEXT DEFAULT 'Pending',  -- Pending, In Progress, Completed
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL,
                    project TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            print("Database initialized successfully.")
        except Error as e:
            print(f"Error during table creation: {e}")
        finally:
            conn.close()
    else:
        print("Error: Cannot create the database connection.")

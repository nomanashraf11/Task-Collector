import sqlite3
from sqlite3 import Error
import os

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
            
        conn = sqlite3.connect('data/task_manager.db')
        return conn
    except Error as e:
        print(e)
    
    return conn

def initialize_database():
    """Initialize the database with required tables."""
    conn = create_connection()
    
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    is_admin INTEGER DEFAULT 0
                )
            ''')
            
            # Create tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority INTEGER DEFAULT 2,  # 1: High, 2: Medium, 3: Low
                    due_date TEXT,
                    status TEXT DEFAULT 'Pending',  # Pending, In Progress, Completed
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL,
                    project TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()
    else:
        print("Error: Cannot create the database connection.")
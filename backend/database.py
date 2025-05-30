import sqlite3
import os

def create_connection():
    if not os.path.exists('data'):
        os.makedirs('data')
    return sqlite3.connect('data/task_manager.db')

def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()
    

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            is_admin INTEGER DEFAULT 0,
            is_manager INTEGER DEFAULT 0  -- New column for manager role
        )
    ''')
    

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority INTEGER DEFAULT 2,
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,  -- The user who needs to complete the task
            assigned_by INTEGER,       -- The manager who assigned the task (NULL if self-created)
            project TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (assigned_by) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
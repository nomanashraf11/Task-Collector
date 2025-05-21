import sqlite3
from backend.models import User

def register_user(username, email, password):
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password, email)
        )
        conn.commit()
        return User(cursor.lastrowid, username, email)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def login_user(username, password):
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password, email, is_admin FROM users WHERE username = ?",
            (username,)
        )
        user_data = cursor.fetchone()
        if user_data and user_data[2] == password:
            return User(user_data[0], user_data[1], user_data[3], bool(user_data[4]))
        return None
    finally:
        conn.close()

def is_admin(user_id):
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT is_admin FROM users WHERE id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return result and bool(result[0])
    finally:
        conn.close()

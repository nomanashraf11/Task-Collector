import sqlite3
from backend.models import User

def register_user(username, email, password, is_manager=False):
    #register user functionality
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email, is_manager) VALUES (?, ?, ?, ?)",
            (username, password, email, is_manager)
        )
        conn.commit()
        return User(cursor.lastrowid, username, email, False, is_manager)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def login_user(username, password):
    #login functionality
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, username, password, email, is_admin ,is_manager FROM users WHERE username = ?",
            (username,)
        )
        user_data = cursor.fetchone()
        print(user_data)

        if not user_data:
            print("User not found.")
            return None

        db_password = user_data[2]

        if db_password != password:
            print("Incorrect password.")
            return None

        return User(user_data[0], user_data[1], user_data[3], bool(user_data[4]),bool(user_data[5]))

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

    finally:
        conn.close()

def is_admin(user_id):
    #check admin
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

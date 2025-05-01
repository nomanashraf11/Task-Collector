import sqlite3
from getpass import getpass
from models import User

def register_user():
    """Register a new user."""
    print("\n--- Register New User ---")
    username = input("Username: ")
    email = input("Email: ")
    password = getpass("Password: ")
    confirm_password = getpass("Confirm Password: ")
    
    if password != confirm_password:
        print("Error: Passwords don't match!")
        return None

    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password, email)
        )
        
        conn.commit()
        print("User registered successfully!")
        return User(cursor.lastrowid, username, email)
    except sqlite3.IntegrityError:
        print("Error: Username or email already exists!")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

def login_user():
    """Login an existing user."""
    print("\n--- Login ---")
    username = input("Username: ")
    password = getpass("Password: ")
    
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, username, password, email, is_admin FROM users WHERE username = ?",
            (username,)
        )
        
        user_data = cursor.fetchone()
        
        if user_data and user_data[2] == password:
            print("Login successful!")
            return User(user_data[0], user_data[1], user_data[3], bool(user_data[4]))
        else:
            print("Invalid username or password!")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

def is_admin(user_id):
    """Check if user is admin."""
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT is_admin FROM users WHERE id = ?",
            (user_id,)
        )
        
        result = cursor.fetchone()
        return result and bool(result[0])
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

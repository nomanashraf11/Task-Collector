import sqlite3
from backend.models import Task

def create_task(title, description, priority, due_date, status, user_id, project=""):
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO tasks 
            (title, description, priority, due_date, status, user_id, project) 
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (title, description, priority, due_date, status, user_id, project)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating task: {e}")
        return False
    finally:
        conn.close()

def view_tasks(user_id, is_admin=False, is_manager=False):
    conn = sqlite3.connect('data/task_manager.db')
    cursor = conn.cursor()
    if is_admin:
        cursor.execute('''
            SELECT id, title, description, priority, due_date, status, user_id, project, created_at
            FROM tasks ORDER BY due_date
        ''')
    elif is_manager:
        # Find user IDs managed by this manager
        cursor.execute("SELECT id FROM users WHERE manager_id = ?", (user_id,))
        managed_ids = [row[0] for row in cursor.fetchall()]
        if managed_ids:
            placeholders = ",".join("?" * len(managed_ids))
            cursor.execute(f"SELECT id, title, description, priority, due_date, status, user_id, project, created_at FROM tasks WHERE user_id IN ({placeholders}) ORDER BY due_date", managed_ids)
        else:
            return []
    else:
        cursor.execute('''
            SELECT id, title, description, priority, due_date, status, user_id, project, created_at
            FROM tasks WHERE user_id = ? ORDER BY due_date
        ''', (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result


def update_task(task_id, title, description, priority, due_date, status, user_id, project=""):
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks 
            SET title = ?, description = ?, priority = ?, due_date = ?, status = ?, project = ?
            WHERE id = ? AND user_id = ?
        ''', (title, description, priority, due_date, status, project, task_id, user_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating task: {e}")
        return False
    finally:
        conn.close()

def delete_task(task_id):
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting task: {e}")
        return False
    finally:
        conn.close()
        
def view_users():
    
    conn = sqlite3.connect('data/task_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_admin FROM users")
    rows = cursor.fetchall()
    conn.close()
    users = [User(r[0], r[1], r[2], bool(r[3])) for r in rows]
    return users
        


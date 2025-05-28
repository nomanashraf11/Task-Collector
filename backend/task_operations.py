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

def view_tasks(user_id, is_admin=False):
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        if is_admin:
            cursor.execute('''
                SELECT id, title, description, priority, due_date, status, user_id, project, created_at
                FROM tasks ORDER BY due_date
            ''')
        else:
            cursor.execute('''
                SELECT id, title, description, priority, due_date, status, user_id, project, created_at
                FROM tasks WHERE user_id = ? ORDER BY due_date
            ''', (user_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error viewing tasks: {e}")
        return []
    finally:
        conn.close()

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

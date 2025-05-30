import sqlite3
from typing import List, Optional
from backend.models import Task, User
import os
def create_connection():
    """Create and return a database connection"""
    if not os.path.exists('data'):
        os.makedirs('data')
    return sqlite3.connect('data/task_manager.db')

def view_tasks(current_user: User) -> List[Task]:
    """Get tasks based on user role and permissions"""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        if current_user.is_admin:
            # Admins see all tasks
            cursor.execute('''
                SELECT id, title, description, priority, due_date, status,
                       user_id, project, created_at, assigned_by
                FROM tasks ORDER BY due_date
            ''')
        elif current_user.is_manager:
            # Managers see:
            # 1. Tasks they assigned to others (assigned_by = manager)
            # 2. Tasks assigned to them (user_id = manager)
            cursor.execute('''
                SELECT id, title, description, priority, due_date, status,
                       user_id, project, created_at, assigned_by
                FROM tasks 
                WHERE user_id = ? OR assigned_by = ?
                ORDER BY due_date
            ''', (current_user.id, current_user.id))
        else:
            # Regular users only see tasks assigned to them (user_id = user)
            cursor.execute('''
                SELECT id, title, description, priority, due_date, status,
                       user_id, project, created_at, assigned_by
                FROM tasks 
                WHERE user_id = ?
                ORDER BY due_date
            ''', (current_user.id,))
            
        return [Task(*row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error viewing tasks: {e}")
        return []
    finally:
        conn.close()

def create_task(
    title: str,
    description: str,
    priority: int,
    due_date: str,
    status: str,
    current_user: User,
    assigned_to: Optional[int] = None,
    project: str = ""
) -> bool:
    """Create task with proper ownership tracking"""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        # Permission check - only managers/admins can assign tasks
        if assigned_to and not (current_user.is_manager or current_user.is_admin):
            print("Error: Only managers/admins can assign tasks")
            return False
            
        # Validate priority
        if priority not in (1, 2, 3):
            raise ValueError("Priority must be 1, 2, or 3")
        
        # Verify assigned_to user exists if specified
        if assigned_to:
            cursor.execute("SELECT 1 FROM users WHERE id = ?", (assigned_to,))
            if not cursor.fetchone():
                print("Error: Target user does not exist")
                return False
        
        # Determine ownership
        assigned_by = current_user.id if assigned_to else None
        actual_user_id = assigned_to if assigned_to else current_user.id
        
        cursor.execute('''
            INSERT INTO tasks 
            (title, description, priority, due_date, status, user_id, project, assigned_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, priority, due_date, status, actual_user_id, project, assigned_by))
        
        conn.commit()
        return True
        
    except ValueError as e:
        print(f"Validation error: {e}")
        return False
    except Exception as e:
        print(f"Error creating task: {e}")
        return False
    finally:
        conn.close()

def update_task(
    task_id: int,
    title: str,
    description: str,
    priority: int,
    due_date: str,
    status: str,
    current_user: User,  # This should be a User object
    project: str = ""
) -> bool:
    """Update task with permission checks"""
    try:
        # Type checking for current_user
        if not isinstance(current_user, User):
            print("Error: current_user must be a User object")
            return False

        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, assigned_by FROM tasks WHERE id = ?
        ''', (task_id,))
        task_data = cursor.fetchone()
        
        if not task_data:
            print("Task not found")
            return False
            
        task_user_id, assigned_by = task_data
        
        # Permission check for each role
        if not (current_user.is_admin or 
                current_user.id == task_user_id or
                (current_user.is_manager and assigned_by == current_user.id)): 
            print("Permission denied")
            return False
            
        if priority not in (1, 2, 3):
            raise ValueError("Priority must be 1, 2, or 3")
            
        cursor.execute('''
            UPDATE tasks 
            SET title = ?, description = ?, priority = ?, due_date = ?, 
                status = ?, project = ?
            WHERE id = ?
        ''', (title, description, priority, due_date, status, project, task_id))
        
        conn.commit()
        return cursor.rowcount > 0
    except ValueError as e:
        print(f"Validation error: {e}")
        return False
    except Exception as e:
        print(f"Error updating task: {e}")
        return False
    finally:
        conn.close()
def delete_task(task_id: int, current_user: User) -> bool:
    """Delete task with permission checks"""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        # First get task details and ownership
        cursor.execute('''
            SELECT user_id, assigned_by FROM tasks WHERE id = ?
        ''', (task_id,))
        task_data = cursor.fetchone()
        
        if not task_data:
            print("Task not found")
            return False
            
        task_user_id, assigned_by = task_data
        
        # Again check the Permission 
        if not (current_user.is_admin or  
                current_user.id == task_user_id or  
                (current_user.is_manager and assigned_by == current_user.id)):  
            print("Permission denied")
            return False
            
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting task: {e}")
        return False
    finally:
        conn.close()
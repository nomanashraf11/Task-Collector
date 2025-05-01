import sqlite3
from datetime import datetime
from models import Task

def create_task(user_id):
    """Create a new task."""
    print("\n--- Create New Task ---")
    title = input("Title: ")
    description = input("Description: ")
    priority = input("Priority (1: High, 2: Medium, 3: Low): ")
    due_date = input("Due date (YYYY-MM-DD): ")
    project = input("Project: ")
    
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT INTO tasks 
            (title, description, priority, due_date, project, user_id) 
            VALUES (?, ?, ?, ?, ?, ?)''',
            (title, description, priority, due_date, project, user_id)
        )
        
        conn.commit()
        print("Task created successfully!")
        return Task(cursor.lastrowid, title, description, priority, due_date, "Pending", user_id, project)
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

def view_tasks(user_id, is_admin=False):
    """View tasks for a user or all tasks if admin."""
    try:
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        print(conn)
        if is_admin:
            cursor.execute(
                '''SELECT id, title, description, priority, due_date, status, project, created_at 
                FROM tasks ORDER BY due_date'''
            )
            print("\n--- All Tasks (Admin View) ---")
        else:
            cursor.execute(
                '''SELECT id, title, description, priority, due_date, status, project, created_at 
                FROM tasks WHERE user_id = ? ORDER BY due_date''',
                (user_id,)
            )
            print("\n--- Your Tasks ---")
        
        tasks = cursor.fetchall()
        
        if not tasks:
            print("No tasks found.")
            return []
        
        for task in tasks:
            print(f"\nTask ID: {task[0]}")
            print(f"Title: {task[1]}")
            print(f"Description: {task[2]}")
            print(f"Priority: {task[3]} ({'High' if task[3] == 1 else 'Medium' if task[3] == 2 else 'Low'})")
            print(f"Due Date: {task[4]}")
            print(f"Status: {task[5]}")
            print(f"Project: {task[6]}")
            print(f"Created At: {task[7]}")
        
        return tasks
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def update_task(user_id, is_admin=False):
    """Update an existing task."""
    tasks = view_tasks(user_id, is_admin)
    if not tasks:
        return
    
    try:
        task_id = int(input("\nEnter Task ID to update: "))
        
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        
        # Check if task exists and belongs to user (unless admin)
        if not is_admin:
            cursor.execute(
                "SELECT id FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )
            if not cursor.fetchone():
                print("Error: Task not found or you don't have permission to edit it.")
                return
        
        print("\nLeave field blank to keep current value.")
        title = input("New Title: ")
        description = input("New Description: ")
        priority = input("New Priority (1: High, 2: Medium, 3: Low): ")
        due_date = input("New Due Date (YYYY-MM-DD): ")
        status = input("New Status (Pending/In Progress/Completed): ")
        project = input("New Project: ")
        
        # Get current values
        cursor.execute(
            "SELECT title, description, priority, due_date, status, project FROM tasks WHERE id = ?",
            (task_id,)
        )
        current = cursor.fetchone()
        
        # Prepare update
        updates = []
        params = []
        
        if title:
            updates.append("title = ?")
            params.append(title)
        else:
            params.append(current[0])
            
        if description:
            updates.append("description = ?")
            params.append(description)
        else:
            params.append(current[1])
            
        if priority:
            updates.append("priority = ?")
            params.append(priority)
        else:
            params.append(current[2])
            
        if due_date:
            updates.append("due_date = ?")
            params.append(due_date)
        else:
            params.append(current[3])
            
        if status:
            updates.append("status = ?")
            params.append(status)
        else:
            params.append(current[4])
            
        if project:
            updates.append("project = ?")
            params.append(project)
        else:
            params.append(current[5])
            
        params.append(task_id)
        
        # Build and execute update query
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        
        conn.commit()
        print("Task updated successfully!")
    except ValueError:
        print("Error: Please enter a valid Task ID.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def delete_task(user_id, is_admin=False):
    """Delete a task."""
    tasks = view_tasks(user_id, is_admin)
    if not tasks:
        return
    
    try:
        task_id = int(input("\nEnter Task ID to delete: "))
        
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        
        # Check if task exists and belongs to user (unless admin)
        if not is_admin:
            cursor.execute(
                "SELECT id FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )
            if not cursor.fetchone():
                print("Error: Task not found or you don't have permission to delete it.")
                return
        
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        print("Task deleted successfully!")
    except ValueError:
        print("Error: Please enter a valid Task ID.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
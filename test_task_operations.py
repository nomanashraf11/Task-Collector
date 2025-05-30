import sqlite3
from backend.models import User
from backend.task_operations import (
    create_task,
    view_tasks,
    update_task,
    delete_task,
    create_connection
)

def setup_test_users():
    """Create test users if they don't exist"""
    test_users = [
        (1, 'admin', 'admin123', 'admin@test.com', 1, 0),
        (2, 'manager', 'manager123', 'manager@test.com', 0, 1),
        (3, 'user1', 'user123', 'user1@test.com', 0, 0),
        (4, 'user2', 'user123', 'user2@test.com', 0, 0)
    ]
    
    conn = create_connection()
    cursor = conn.cursor()
    
    for user in test_users:
        cursor.execute('''
            INSERT OR IGNORE INTO users 
            (id, username, password, email, is_admin, is_manager)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', user)
    
    conn.commit()
    conn.close()

def clean_test_tasks():
    """Remove all test tasks"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()

def test_task_operations():
    """Test all task operations with role-based permissions"""
    # Setup test environment
    setup_test_users()
    clean_test_tasks()
    
    # Test users
    admin = User(id=1, username="admin", email="admin@test.com", is_admin=True)
    manager = User(id=2, username="manager", email="manager@test.com", is_manager=True)
    user1 = User(id=3, username="user1", email="user1@test.com")
    user2 = User(id=4, username="user2", email="user2@test.com")

    # Test 1: Admin creates task for self
    print("\nTest 1: Admin creates self-task")
    assert create_task(
        title="Admin self-task",
        description="Admin working directly",
        priority=1,
        due_date="2023-12-31",
        status="Pending",
        current_user=admin
    ), "Admin should create self-task"

    # Test 2: Admin assigns task to user1
    print("\nTest 2: Admin assigns task to user1")
    assert create_task(
        title="Admin assigned task",
        description="User must complete this",
        priority=2,
        due_date="2023-12-15",
        status="Pending",
        current_user=admin,
        assigned_to=user1.id
    ), "Admin should assign tasks"

    # Test 3: Manager creates task for self
    print("\nTest 3: Manager creates self-task")
    assert create_task(
        title="Manager self-task",
        description="Manager working directly",
        priority=2,
        due_date="2023-12-20",
        status="In Progress",
        current_user=manager
    ), "Manager should create self-task"

    # Test 4: Manager assigns task to user2
    print("\nTest 4: Manager assigns task")
    assert create_task(
        title="Manager assigned task",
        description="User must complete this",
        priority=3,
        due_date="2023-12-10",
        status="Pending",
        current_user=manager,
        assigned_to=user2.id
    ), "Manager should assign tasks"

    # Test 5: Regular user creates task
    print("\nTest 5: User creates self-task")
    assert create_task(
        title="User personal task",
        description="Working on my stuff",
        priority=1,
        due_date="2023-12-25",
        status="Pending",
        current_user=user1
    ), "User should create self-task"

    print("\nTest 5a: User tries to assign task (should fail)")
    assert not create_task(
        title="Illegal assignment",
        description="User shouldn't do this",
        priority=1,
        due_date="2023-12-25",
        status="Pending",
        current_user=user1,
        assigned_to=user2.id
    ), "Regular user shouldn't assign tasks"

    # Verify task visibility
    print("\nVerifying task visibility...")
    admin_tasks = view_tasks(admin)
    print(f"Admin sees {len(admin_tasks)} tasks (should see all)")
    assert len(admin_tasks) == 5, "Admin should see all tasks"

    manager_tasks = view_tasks(manager)
    print(f"Manager sees {len(manager_tasks)} tasks (should see their tasks)")
    assert len(manager_tasks) == 3, "Manager should see their tasks"

    user1_tasks = view_tasks(user1)
    print(f"User1 sees {len(user1_tasks)} tasks (should see only theirs)")
    assert len(user1_tasks) == 2, "User should see their assigned and self-created tasks"

    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_task_operations()
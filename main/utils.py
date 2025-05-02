def display_menu(user, is_admin=False):
    print("\n--- Task Manager ---")
    print(f"Logged in as: {user.username} ({'Admin' if is_admin else 'User'})")
    print("\n1. View Tasks")
    print("2. Create Task")
    print("3. Update Task")
    print("4. Delete Task")
    if is_admin:
        print("5. View All Users' Tasks")
    print("0. Logout")
    try:
        choice = int(input("\nEnter your choice: "))
        return choice
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None
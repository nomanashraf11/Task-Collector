from auth import login_user, register_user, is_admin
from task_operations import create_task, view_tasks, update_task, delete_task
from utils import display_menu
from database import initialize_database

def main():

    initialize_database()
    
    current_user = None
    
    while True:
        if not current_user:
            print("\n=== Task Management System ===")
            print("1. Login")
            print("2. Register")
            print("0. Exit")
            
            try:
                choice = int(input("\nEnter your choice: "))
                
                if choice == 1:
                    current_user = login_user()
                elif choice == 2:
                    current_user = register_user()
                elif choice == 0:
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            user_is_admin = is_admin(current_user.id)
            choice = display_menu(current_user, user_is_admin)
            
            if choice == 0:
                current_user = None
                print("Logged out successfully!")
            elif choice == 1:
                view_tasks(current_user.id)
            elif choice == 2:
                create_task(current_user.id)
            elif choice == 3:
                update_task(current_user.id)
            elif choice == 4:
                delete_task(current_user.id)
            elif choice == 5 and user_is_admin:
                view_tasks(current_user.id, is_admin=True)
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
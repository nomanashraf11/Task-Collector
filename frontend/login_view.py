import tkinter as tk
from tkinter import ttk, messagebox
from backend.auth import login_user

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Making FRAME fill the whole available space
        self.grid(row=0, column=0, sticky="nsew")
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)

        # Centering the form
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        content = ttk.Frame(container)
        content.grid(row=0, column=0)
        content.columnconfigure(0, weight=1)

        # Title of the page
        ttk.Label(content, text="TASK COLLECTOR(LOGIN)", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username
        ttk.Label(content, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.username = ttk.Entry(content, font=("Arial", 12), width=25)
        self.username.grid(row=1, column=1, padx=5, pady=5)
        # Password
        ttk.Label(content, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password = ttk.Entry(content, show="*", font=("Arial", 12), width=25)
        self.password.grid(row=2, column=1, padx=5, pady=5)
        # Login Button
        ttk.Button(content, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=(15, 5))

        # Register Button
        ttk.Button(content, text="Register", command=lambda: controller.show_frame("RegisterFrame")).grid(row=4, column=0, columnspan=2)

     

    def login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing Fields", "Please enter both username and password.")
            return

        user = login_user(username, password)
        if user:
            self.controller.current_user = user
            print(user,"user")
            #assign role for conditional rendering
            if user.is_admin:
                self.controller.user_role = 'admin'
            elif user.is_manager:
                self.controller.user_role = 'manager'
            else:
                self.controller.user_role = 'regular'
            self.controller.show_frame("TaskFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")
            self.password.delete(0, tk.END)

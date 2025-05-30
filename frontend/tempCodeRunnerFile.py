import tkinter as tk
from tkinter import ttk, messagebox
from backend.auth import login_user

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
    
        container = ttk.Frame(self)
        container.pack(expand=True, fill="both", padx=20, pady=20)
        
       
        ttk.Label(container, text="Login", font=("Arial", 16)).pack(pady=10)
        
        
        form = ttk.Frame(container)
        form.pack(pady=20)
        
       
        username_frame = ttk.Frame(form)
        username_frame.pack(fill="x", pady=5)
        ttk.Label(username_frame, text="Username:").pack(side="left", padx=5)
        self.username = ttk.Entry(username_frame)
        self.username.pack(side="left", expand=True, fill="x")
        
    
        password_frame = ttk.Frame(form)
        password_frame.pack(fill="x", pady=5)
        ttk.Label(password_frame, text="Password:").pack(side="left", padx=5)
        self.password = ttk.Entry(password_frame, show="*")
        self.password.pack(side="left", expand=True, fill="x")
        
        # Buttons frame
        buttons_frame = ttk.Frame(container)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Login", command=self.login).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Register", 
                  command=lambda: controller.show_frame("RegisterFrame")).pack(side="left", padx=5)
    
    def login(self):
        username = self.username.get()
        password = self.password.get()
        user = login_user(username, password)
        if user:
            self.controller.current_user = user
            self.controller.show_frame("TaskFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")
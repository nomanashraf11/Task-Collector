import tkinter as tk
from tkinter import ttk, messagebox
from backend.auth import login_user

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Login", font=("Arial", 16)).pack(pady=10)
        form = ttk.Frame(self)
        form.pack(pady=20)
        ttk.Label(form, text="Username:").grid(row=0, column=0)
        self.username = ttk.Entry(form)
        self.username.grid(row=0, column=1)
        ttk.Label(form, text="Password:").grid(row=1, column=0)
        self.password = ttk.Entry(form, show="*")
        self.password.grid(row=1, column=1)
        ttk.Button(self, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterFrame")).pack()
    
    def login(self):
        username = self.username.get()
        password = self.password.get()
        user = login_user(username, password)
        if user:
            self.controller.current_user = user
            self.controller.show_frame("TaskFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

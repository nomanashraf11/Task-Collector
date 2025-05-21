import tkinter as tk
from tkinter import ttk, messagebox
from backend.auth import register_user

class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Register", font=("Arial", 16)).pack(pady=10)
        form = ttk.Frame(self)
        form.pack(pady=20)
        ttk.Label(form, text="Username:").grid(row=0, column=0)
        self.username = ttk.Entry(form)
        self.username.grid(row=0, column=1)
        ttk.Label(form, text="Email:").grid(row=1, column=0)
        self.email = ttk.Entry(form)
        self.email.grid(row=1, column=1)
        ttk.Label(form, text="Password:").grid(row=2, column=0)
        self.password = ttk.Entry(form, show="*")
        self.password.grid(row=2, column=1)
        ttk.Label(form, text="Confirm:").grid(row=3, column=0)
        self.confirm = ttk.Entry(form, show="*")
        self.confirm.grid(row=3, column=1)
        ttk.Button(self, text="Register", command=self.register).pack(pady=10)
        ttk.Button(self, text="Back to Login", command=lambda: controller.show_frame("LoginFrame")).pack()
    
    def register(self):
        username = self.username.get()
        email = self.email.get()
        password = self.password.get()
        confirm = self.confirm.get()
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        user = register_user(username, email, password)
        if user:
            self.controller.current_user = user
            self.controller.show_frame("TaskFrame")
        else:
            messagebox.showerror("Error", "Registration failed (username/email may exist).")

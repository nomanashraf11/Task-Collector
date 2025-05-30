import tkinter as tk
from tkinter import ttk, messagebox
from backend.auth import register_user

class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.after(100, lambda: self.center_frame())
        self.create_widgets()
    
    def create_widgets(self):
        ttk.Label(self, text="Register New User", font=("Arial", 16)).pack(pady=20)
        form = ttk.Frame(self)
        form.pack(pady=20, padx=40, fill=tk.X)

        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username = ttk.Entry(form)
        self.username.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email = ttk.Entry(form)
        self.email.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password = ttk.Entry(form, show="*")
        self.password.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form, text="Confirm Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.confirm = ttk.Entry(form, show="*")
        self.confirm.grid(row=3, column=1, pady=5, padx=5)

        form.columnconfigure(1, weight=1)
        buttons = ttk.Frame(self)
        buttons.pack(pady=20)
        ttk.Button(buttons, text="Register", command=self.register).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons, text="Back", command=lambda: self.controller.show_frame("LoginFrame")).pack(side=tk.LEFT, padx=5)
    
    def center_frame(self):
        w = 400
        h = 310
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.controller.geometry(f'{w}x{h}+{x}+{y}')
    
    def register(self):
        username = self.username.get()
        email = self.email.get()
        password = self.password.get()
        confirm = self.confirm.get()
        if not username or not email or not password or not confirm:
            messagebox.showerror("Error", "All fields are required.")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        user = register_user(username, email, password)
        if user:
            self.controller.current_user = user
            self.controller.show_frame("TaskFrame")
        else:
            messagebox.showerror("Error", "Registration failed (username/email may exist).")

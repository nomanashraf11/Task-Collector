import tkinter as tk
from tkinter import ttk, messagebox
from backend.auth import login_user

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        controller.after(100, lambda: self.center_frame())  # Center after widget creation
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Task Manager Login", font=("Arial", 16)).pack(pady=20)
        form = ttk.Frame(self)
        form.pack(pady=20, padx=40, fill=tk.X)

        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username = ttk.Entry(form)
        self.username.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password = ttk.Entry(form, show="*")
        self.password.grid(row=1, column=1, pady=5, padx=5)

        form.columnconfigure(1, weight=1)
        buttons = ttk.Frame(self)
        buttons.pack(pady=20)
        ttk.Button(buttons, text="Login", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons, text="Register", command=lambda: self.controller.show_frame("RegisterFrame")).pack(side=tk.LEFT, padx=5)

    def center_frame(self):
        w = 350
        h = 250
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.controller.geometry(f'{w}x{h}+{x}+{y}')

    def login(self):
        username = self.username.get()
        password = self.password.get()
        user = login_user(username, password)
        if user:
            self.controller.current_user = user
            # Redirect based on role
            if user.is_admin:
                self.controller.show_frame("AdminFrame")
            elif user.role == "manager":
                self.controller.show_frame("ManagerFrame")
            else:
                self.controller.show_frame("TaskFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

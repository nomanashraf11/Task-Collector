import tkinter as tk
from tkinter import ttk, messagebox

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        ttk.Label(self, text="Task Manager Login", style='Header.TLabel').pack(pady=20)
        
        # Form
        form = ttk.Frame(self)
        form.pack(pady=20, padx=50, fill=tk.X)
        
        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username = ttk.Entry(form)
        self.username.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(form, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password = ttk.Entry(form, show="*")
        self.password.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        form.columnconfigure(1, weight=1)
        
        # Buttons
        buttons = ttk.Frame(self)
        buttons.pack(pady=20)
        
        ttk.Button(buttons, text="Login", command=self.on_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons, text="Register", command=self.on_register).pack(side=tk.LEFT, padx=5)
    
    def on_login(self):
        if self.controller.login(self.username.get(), self.password.get()):
            messagebox.showinfo("Success", "Login successful")
        else:
            messagebox.showerror("Error", "Invalid credentials")
            self.password.delete(0, tk.END)
    
    def on_register(self):
        self.controller.show_frame(RegisterFrame)

class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):

        ttk.Label(self, text="Register New User", style='Header.TLabel').pack(pady=20)
        
 
        form = ttk.Frame(self)
        form.pack(pady=20, padx=50, fill=tk.X)
        
        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username = ttk.Entry(form)
        self.username.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(form, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email = ttk.Entry(form)
        self.email.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(form, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password = ttk.Entry(form, show="*")
        self.password.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(form, text="Confirm Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.confirm = ttk.Entry(form, show="*")
        self.confirm.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        
        form.columnconfigure(1, weight=1)
        
       
        buttons = ttk.Frame(self)
        buttons.pack(pady=20)
        
        ttk.Button(buttons, text="Register", command=self.on_register).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons, text="Back", command=self.on_back).pack(side=tk.LEFT, padx=5)
    
    def on_register(self):
        if self.controller.register(
            self.username.get(),
            self.email.get(),
            self.password.get(),
            self.confirm.get()
        ):
            messagebox.showinfo("Success", "Registration successful")
        else:
            messagebox.showerror("Error", "Registration failed")
    
    def on_back(self):
        self.controller.show_frame(LoginFrame)
import tkinter as tk
from tkinter import ttk, messagebox
from backend.auth import register_user

class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure the frame 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # centered main container
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        # Center frame centering
        center_frame = ttk.Frame(container)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
  
                 
        ttk.Label(center_frame, text="Register", font=("Arial", 16)).grid(
            row=0, column=0, columnspan=2, pady=(0, 20))
        
      
        fields = [
            ("Username:", "username", ""),
            ("Email:", "email", ""),
            ("Password:", "password", "*"),
            ("Confirm:", "confirm", "*")
        ]
        
        self.entries = {}
        for row, (label_text, entry_name, show_char) in enumerate(fields, start=1):
            # Label
            ttk.Label(center_frame, text=label_text).grid(
                row=row, column=0, padx=5, pady=5, sticky="e")
            
            # Entry field
            entry = ttk.Entry(center_frame, show=show_char, width=25)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.entries[entry_name] = entry
        
        # Buttons frame
        buttons_frame = ttk.Frame(center_frame)
        buttons_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(buttons_frame, text="Register", 
                 command=self.register).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Back to Login", 
                 command=lambda: controller.show_frame("LoginFrame")).pack(side="left", padx=5)
    
    def register(self):
        username = self.entries["username"].get()
        email = self.entries["email"].get()
        password = self.entries["password"].get()
        confirm = self.entries["confirm"].get()
        
        if not all([username, email, password, confirm]):
            messagebox.showerror("Error", "All fields are required!")
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
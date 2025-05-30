import tkinter as tk
from tkinter import ttk, messagebox
from backend.task_operations import view_tasks, create_task, update_task, delete_task
import sqlite3
class TaskFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Title Frame
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill=tk.X, pady=10)
        
        # Main title
        ttk.Label(self.title_frame, text="Task Manager", font=("Arial", 16)).pack(side=tk.LEFT)
        
   
        self.user_info_label = ttk.Label(self.title_frame, text="", font=("Arial", 10))
        self.user_info_label.pack(side=tk.RIGHT, padx=10)
        
        # Treeview setup
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Priority", "Due Date", "Status"), show="headings")
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Title", width=200, anchor=tk.CENTER)
        self.tree.column("Priority", width=80, anchor=tk.CENTER)
        self.tree.column("Due Date", width=100, anchor=tk.CENTER)
        self.tree.column("Status", width=100, anchor=tk.CENTER)
        
        for col in ("ID", "Title", "Priority", "Due Date", "Status"):
            self.tree.heading(col, text=col, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Button frame
        self.btn_frame = ttk.Frame(self)
        self.btn_frame.pack(pady=10)
        
    
        self.add_btn = ttk.Button(self.btn_frame, text="Add Task", command=self.add_task)
        self.edit_btn = ttk.Button(self.btn_frame, text="Edit Task", command=self.edit_task)
        self.delete_btn = ttk.Button(self.btn_frame, text="Delete Task", command=self.delete_task_ui)
        self.logout_btn = ttk.Button(self.btn_frame, text="Logout", command=self.logout)
        
        self.bind("<Visibility>", lambda e: self.refresh_tasks())

    def refresh_tasks(self):
        if self.controller.current_user is None:
            return
            
        # Update user can see info display
        self.user_info_label.config(
            text=f"Logged in as: {self.controller.current_user.username} ({self.controller.user_role})"
        )
        
        # Clear and repopulate tasks so we role dont get confused
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        tasks = view_tasks(self.controller.current_user)
        for t in tasks:
            self.tree.insert("", tk.END, values=(t.id, t.title, t.priority, t.due_date, t.status))
        
        # Clear all buttons first
        for btn in self.btn_frame.winfo_children():
            btn.pack_forget()
        
        if self.controller.user_role == 'admin':
            self.add_btn.pack(side=tk.LEFT, padx=5)
            self.edit_btn.pack(side=tk.LEFT, padx=5)
            self.delete_btn.pack(side=tk.LEFT, padx=5)
 
        elif self.controller.user_role == 'manager':
            self.add_btn.pack(side=tk.LEFT, padx=5)
            self.edit_btn.pack(side=tk.LEFT, padx=5)
            self.delete_btn.pack(side=tk.LEFT, padx=5)
       
        else:
            self.edit_btn.pack(side=tk.LEFT, padx=5)
            
        self.logout_btn.pack(side=tk.LEFT, padx=5)
        
    def add_task(self):
        win = tk.Toplevel(self)
        win.title("Add Task")
        
        fields = [
            ("Title:", "title"),
            ("Description:", "desc"),
            ("Priority (1-3):", "priority"),
            ("Due Date (YYYY-MM-DD):", "due_date"),
            ("Status:", "status")
        ]
        
        entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(win, text=label).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            entry = ttk.Entry(win)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field] = entry
        
        # Add user assignment dropdown for manafers and admin
        if self.controller.user_role in ('admin', 'manager'):
            ttk.Label(win, text="Assign To:").grid(row=len(fields), column=0, sticky=tk.E, padx=5, pady=5)
            users = self.get_all_users()
            assign_var = tk.StringVar(value=self.controller.current_user.username)
            assign_dropdown = ttk.Combobox(win, textvariable=assign_var, values=users)
            assign_dropdown.grid(row=len(fields), column=1, padx=5, pady=5)
        
        def save():
            task_data = {
                'title': entries['title'].get(),
                'description': entries['desc'].get(),
                'priority': int(entries['priority'].get()),
                'due_date': entries['due_date'].get(),
                'status': entries['status'].get(),
                'current_user': self.controller.current_user
            }
            
            if self.controller.user_role in ('admin', 'manager'):
                assigned_to = self.get_user_id(assign_var.get())
                task_data['assigned_to'] = assigned_to
            
            if create_task(**task_data):
                self.refresh_tasks()
                win.destroy()
        
        ttk.Button(win, text="Save", command=save).grid(row=len(fields)+1, columnspan=2, pady=10)

    def get_all_users(self):
        """Fetch all users for assignment dropdown"""
        conn = sqlite3.connect('data/task_manager.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users")
        users = [f"{row[1]} (ID:{row[0]})" for row in cursor.fetchall()]
        conn.close()
        return users

    def get_user_id(self, username_with_id):
        """Extract user ID from dropdown selection"""
        return int(username_with_id.split("ID:")[1].rstrip(")"))

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to edit.")
            return
        item = self.tree.item(selected[0])
        task_id = item["values"][0]
        win = tk.Toplevel(self)
        win.title("Edit Task")
        ttk.Label(win, text="Title:").grid(row=0, column=0)
        title_entry = ttk.Entry(win)
        title_entry.insert(0, item["values"][1])
        title_entry.grid(row=0, column=1)
        ttk.Label(win, text="Priority (1-3):").grid(row=1, column=0)
        prio_entry = ttk.Entry(win)
        prio_entry.insert(0, item["values"][2])
        prio_entry.grid(row=1, column=1)
        ttk.Label(win, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0)
        due_entry = ttk.Entry(win)
        due_entry.insert(0, item["values"][3])
        due_entry.grid(row=2, column=1)
        ttk.Label(win, text="Status:").grid(row=3, column=0)
        status_entry = ttk.Entry(win)
        status_entry.insert(0, item["values"][4])
        status_entry.grid(row=3, column=1)

        def save():
            title = title_entry.get()
            desc = ""  
            prio = int(prio_entry.get())
            due = due_entry.get()
            status = status_entry.get()
            if update_task(task_id, title, desc, prio, due, status, self.controller.current_user.id):
                self.refresh_tasks()
                win.destroy()
            else:
                messagebox.showerror("Error", "Failed to update task.")

        ttk.Button(win, text="Save", command=save).grid(row=4, columnspan=2)

    def delete_task_ui(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to delete.")
            return
        item = self.tree.item(selected[0])
        task_id = item["values"][0]
        if messagebox.askyesno("Delete", "Delete this task?"):
            if delete_task(task_id, self.controller.current_user):  # Pass current_user
                self.refresh_tasks()
            else:
                messagebox.showerror("Error", "Failed to delete task - check permissions")

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginFrame")

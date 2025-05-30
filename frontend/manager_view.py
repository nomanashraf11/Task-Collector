import tkinter as tk
from tkinter import ttk, messagebox
from backend.task_operations import view_users, view_tasks

class ManagerView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Manager Dashboard", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("ID", "Username", "Email"), show="headings")
        for col in ("ID", "Username", "Email"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_users).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View User Tasks", command=self.view_selected_user_tasks).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Logout", command=self.logout).pack(side=tk.LEFT, padx=5)
        self.refresh_users()

    def refresh_users(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for u in view_users():
            self.tree.insert("", tk.END, values=(u.id, u.username, u.email))

    def view_selected_user_tasks(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("No user selected", "Please select a user.")
            return
        user_id, username, *_ = self.tree.item(sel[0])["values"]
        win = tk.Toplevel(self)
        win.title(f"{username}'s Tasks")
        tree = ttk.Treeview(win, columns=("ID", "Title", "Priority", "Due Date", "Status"), show="headings")
        for col in ("ID", "Title", "Priority", "Due Date", "Status"):
            tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True)
        tasks = view_tasks(user_id, is_admin=True)
        for t in tasks:
            tree.insert("", tk.END, values=(t[0], t[1], t[3], t[4], t[5]))

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginFrame")

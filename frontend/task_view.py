import tkinter as tk
from tkinter import ttk, messagebox
from backend.task_operations import view_tasks, create_task, update_task, delete_task

class TaskFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Task Manager", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Priority", "Due Date", "Status"), show="headings")
        for col in ("ID", "Title", "Priority", "Due Date", "Status"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Task", command=self.delete_task_ui).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Logout", command=self.logout).pack(side=tk.LEFT, padx=5)
         

    def refresh_tasks(self):
         
        if self.controller.current_user is None:
            return   
        for i in self.tree.get_children():
            self.tree.delete(i)
        tasks = view_tasks(self.controller.current_user.id)
        for t in tasks:
            self.tree.insert("", tk.END, values=(t[0], t[1], t[3], t[4], t[5]))

    def add_task(self):
        win = tk.Toplevel(self)
        win.title("Add Task")
        ttk.Label(win, text="Title:").grid(row=0, column=0)
        title_entry = ttk.Entry(win)
        title_entry.grid(row=0, column=1)
        ttk.Label(win, text="Description:").grid(row=1, column=0)
        desc_entry = ttk.Entry(win)
        desc_entry.grid(row=1, column=1)
        ttk.Label(win, text="Priority (1-3):").grid(row=2, column=0)
        prio_entry = ttk.Entry(win)
        prio_entry.grid(row=2, column=1)
        ttk.Label(win, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0)
        due_entry = ttk.Entry(win)
        due_entry.grid(row=3, column=1)
        ttk.Label(win, text="Status:").grid(row=4, column=0)
        status_entry = ttk.Entry(win)
        status_entry.grid(row=4, column=1)

        def save():
            title = title_entry.get()
            desc = desc_entry.get()
            prio = int(prio_entry.get())
            due = due_entry.get()
            status = status_entry.get()
            if create_task(title, desc, prio, due, status, self.controller.current_user.id):
                self.refresh_tasks()
                win.destroy()
            else:
                messagebox.showerror("Error", "Failed to add task.")
        ttk.Button(win, text="Save", command=save).grid(row=5, columnspan=2)

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
            if delete_task(task_id):
                self.refresh_tasks()
            else:
                messagebox.showerror("Error", "Failed to delete task.")

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginFrame")

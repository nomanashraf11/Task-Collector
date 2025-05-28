import tkinter as tk
from tkinter import ttk
from backend.database import initialize_database
from frontend.login_view import LoginFrame
from frontend.register_view import RegisterFrame
from frontend.task_view import TaskFrame

class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        initialize_database()
        self.title("Task Manager")
        self.geometry("700x500")
        self.current_user = None

        self.frames = {}
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)
        for F in (LoginFrame, RegisterFrame, TaskFrame):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("LoginFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if name == "TaskFrame" and self.current_user is not None:
            frame.refresh_tasks()


if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()

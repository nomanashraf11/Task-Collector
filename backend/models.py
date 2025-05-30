from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    email: str
    is_admin: bool = False
    role: str = "user"
    manager_id: int = None

@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: int
    due_date: str
    status: str
    user_id: int
    project: str = ""
    created_at: str = None

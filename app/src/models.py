from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class TaskStatus(str, Enum):
    pending = "pending"
    done = "done"

class TaskCreate(BaseModel):
    title: str
    owner_id: int

class Task(BaseModel):
    id: int
    title: str
    status: TaskStatus
    created_at: datetime
    owner_id: int
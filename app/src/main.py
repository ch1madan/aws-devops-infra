from datetime import datetime
from fastapi import FastAPI
from models import Task, TaskCreate, TaskStatus

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    return Task(
        id=1,
        title=task.title,
        status=TaskStatus.pending,
        created_at=datetime.now(timezone.utc),
        owner_id=task.owner_id,
    )
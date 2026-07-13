from datetime import datetime

from fastapi import FastAPI, HTTPException

from db import get_connection
from models import Task, TaskCreate, TaskStatus

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    created_at = datetime.utcnow()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO tasks (
                        title,
                        status,
                        created_at,
                        owner_id
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        task.title,
                        TaskStatus.pending.value,
                        created_at,
                        task.owner_id,
                    ),
                )

                task_id = cur.fetchone()[0]
                conn.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Task(
        id=task_id,
        title=task.title,
        status=TaskStatus.pending,
        created_at=created_at,
        owner_id=task.owner_id,
    )


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        title,
                        status,
                        created_at,
                        owner_id
                    FROM tasks
                    ORDER BY id
                    """
                )

                rows = cur.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return [
        Task(
            id=row[0],
            title=row[1],
            status=TaskStatus(row[2]),
            created_at=row[3],
            owner_id=row[4],
        )
        for row in rows
    ]
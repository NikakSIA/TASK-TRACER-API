#python -m uvicorn main:app --reload
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

class taskCreate(BaseModel):
    text: str
class Task(BaseModel):
    id: int
    text: str
    completed: bool
    created_at: str
class taskUpdate(BaseModel):
    text: str | None = None
    completed: bool | None = None

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY
AUTOINCREMENT ,
    text TEXT ,
    completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0, 1)) ,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

app = FastAPI()

@app.get("/")
def root():
    return "ok"

@app.get("/tasks", response_model=list[Task])
def get_tasks(completed: None | bool = None, search: str = "", sort_by: Literal["text", "created_at"] = "created_at", order: Literal["ASC", "DESC"] = "DESC"):
    pattern = f"%{search}%"
    if completed is None:
        cursor.execute(f"SELECT id, text, completed, created_at FROM tasks WHERE text LIKE ? ORDER BY {sort_by} {order}", (pattern,))
    else:
        cursor.execute(f"SELECT id, text, completed, created_at FROM tasks WHERE completed = ? AND text LIKE ? ORDER BY {sort_by} {order}", (completed, pattern,))
    rows = cursor.fetchall()
    return [Task(id=row[0], text=row[1], completed=row[2], created_at=row[3]) for row in rows]


@app.post("/tasks")
def create_task(task: taskCreate):
    cursor.execute("INSERT INTO tasks (text) VALUES (?)", (task.text,))
    conn.commit()
    return task.text

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    if cursor.rowcount == 0:
        return {"error": "id was not found"}
    else:
        return {"status": "deleted"}

@app.patch("/tasks/{task_id}")
def complete_task(task_id: int, task_update: taskUpdate):
    if task_update.completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id=?", (task_update.completed, task_id,))
    if task_update.text is not None:
        cursor.execute("UPDATE tasks SET text = ? WHERE id=?", (task_update.text, task_id,))
    conn.commit()
    if cursor.rowcount == 0:
        return {"error": "id was not found"}
    else:
        return {"status": "patched"}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    task_name: str
    completed: bool = False

task_list = []

@app.post("/tasks/")
async def create_task(task: Task):
    task_list.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return task_list

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    if 0 <= task_id < len(task_list):
        task_list[task_id] = task
        return {"message": "Task updated successfully"}
    else:
        return {"error": "Task not found"}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    if 0 <= task_id < len(task_list):
        del task_list[task_id]
        return {"message": "Task deleted successfully"}
    else:
        return {"error": "Task not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
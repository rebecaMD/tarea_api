import pandas as pd
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import joblib

app = FastAPI()

users = []

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: str

tasks = []

@app.post("/register")
async def register_user(username: str, email: str, password: str):
    for user in users:
        if user["username"] == username:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
        if user["email"] == email:
            raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")

    new_user = {"username": username, "email": email, "password": password}
    users.append(new_user)

    return {"message": "Usuario registrado exitosamente"}

@app.post("/tasks/create", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)






import pandas as pd
from fastapi import FastAPI, status, HTTPException, Path
from pydantic import BaseModel
from typing import Optional, List
import joblib

app = FastAPI(
    title="APIs en clase de Mlops 5",
    version="0.0.1"
)

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

@app.get("/tasks/{user_id}")
async def get_task_by_user(user_id: str):
    """

    :type user_id:
    """
    if user_id not in create_task:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return create_task[user_id]

tasks = {
    1: ["Tarea 1", "Tarea 2", "Tarea 3"],
    2: ["Tarea 4", "Tarea 5"]
}

@app.get("/tasks/{user_id}")
async def get_tasks(user_id: int = Path(..., title="ID del usuario", description="ID del usuario para obtener sus tareas")):
    if user_id in tasks:
        return {"Descripción": "Devuelve todas las tareas asociadas a un mismo usuario.",
                "Ejemplo": {"Endpoint": f"/tasks/{user_id}"},
                "Parámetros": {"ID del usuario": user_id},
                "Respuesta": {"Lista de tareas del usuario especificado": tasks[user_id]}}
    else:
        return {"error": "Usuario no encontrado"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



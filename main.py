import pandas as pd
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import joblib

app = FastAPI()

users = []

@app.post("/register")
async def register_user(username: str, email: str, password: str):

    for user in users:
        if user["username"] == username:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
        if user["email"] == email:
            raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")

    class Task(BaseModel):
        title: str
        description: Optional[str] = None
        status: str


    tasks = []

    @app.post("/tasks/create", response_model=Task)
    async def create_task(task: Task):

        tasks.append(task)

        return task

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)


    new_user = {"username": username, "email": email, "password": password}
    users.append(new_user)

    return {"message": "Usuario registrado exitosamente"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


def get_user_by_id(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return None

@app.get("/user/{user_id}")
async def get_user(user_id: int):

    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

class Task(BaseModel):
    title: str
    description: str
    status: str
    user_id: int

tasks = []

def get_tasks_by_user(user_id):
    user_tasks = []
    for task in tasks:
        if task.user_id == user_id:
            user_tasks.append(task)
    return user_tasks

@app.get("/tasks/{user_id}", response_model=List[Task])
async def list_tasks_by_user(user_id: int):
    # Buscamos las tareas asociadas al ID del usuario
    user_tasks = get_tasks_by_user(user_id)
    if not user_tasks:
        raise HTTPException(status_code=404, detail="No se encontraron tareas para este usuario")

    return user_tasks

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


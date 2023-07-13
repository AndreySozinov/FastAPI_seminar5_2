# Создать API для управления списком задач. Приложение должно иметь
# возможность создавать, обновлять, удалять и получать список задач.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс Task с полями id, title, description и status.
# 📌 Создайте список tasks для хранения задач.
# 📌 Создайте маршрут для получения списка задач (метод GET).
# 📌 Создайте маршрут для создания новой задачи (метод POST).
# 📌 Создайте маршрут для обновления задачи (метод PUT).
# 📌 Создайте маршрут для удаления задачи (метод DELETE).
# 📌 Реализуйте валидацию данных запроса и ответа.
import logging
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Optional[str] = None


class TaskForm(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = None


tasks = []


@app.get('/')
async def index():
    logger.info('Отработал GET запрос.')
    return {"message": "Task list manager"}


@app.get('/tasks', response_model=list[Task], summary='Получение списка задач')
async def read_list():
    logger.info('Отработал GET запрос.')
    return tasks


@app.post("/tasks", response_model=Task, summary='Добавление новой задачи')
async def create_task(task: TaskForm):
    new_task_id = 1
    if tasks:
        new_task_id = max(tasks, key=lambda x: x.id).id + 1
    new_task = Task(id=new_task_id, title=task.title, description=task.description, status=task.status)
    tasks.append(new_task)
    logger.info('Отработал POST запрос.')
    return new_task


@app.put('/tasks/{task_id}', response_model=Task, summary='Изменение информации о задаче')
async def update_task(task_id: int, task: TaskForm):
    for el in tasks:
        if el.id == task_id:
            el.title = task.title
            el.description = task.description
            el.status = task.status
            logger.info(f'Отработал PUT запрос для task id = {task_id}.')
            return el
    raise HTTPException(status_code=404, detail='Task with this ID not found')


@app.delete('/tasks/{task_id}', summary='Удаление задачи')
async def delete_task(task_id: int):
    for el in tasks:
        if el.id == task_id:
            tasks.remove(el)
            logger.info(f'Отработал DELETE запрос для task id = {task_id}.')
            return
    raise HTTPException(status_code=404, detail='Task with this ID not found')

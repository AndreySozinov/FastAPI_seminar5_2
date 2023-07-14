"""
Создать RESTful API для управления списком задач. Приложение должно
использовать FastAPI и поддерживать следующие функции:
○ Получение списка всех задач.
○ Получение информации о задаче по её ID.
○ Добавление новой задачи.
○ Обновление информации о задаче по её ID.
○ Удаление задачи по её ID.
📌 Каждая задача должна содержать следующие поля: ID (целое число),
Название (строка), Описание (строка), Статус (строка): "todo", "in progress", "done".
Создайте модуль приложения и настройте сервер и маршрутизацию.
📌 Создайте класс Task с полями id, title, description и status.
📌 Создайте список tasks для хранения задач.
📌 Создайте функцию get_tasks для получения списка всех задач (метод GET).
📌 Создайте функцию get_task для получения информации о задаче по её ID
(метод GET).
📌 Создайте функцию create_task для добавления новой задачи (метод POST).
📌 Создайте функцию update_task для обновления информации о задаче по её ID
(метод PUT).
📌 Создайте функцию delete_task для удаления задачи по её ID (метод DELETE).
"""
from enum import Enum
import logging
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class Status(str, Enum):
    ToDo = 'todo'
    InProgress = 'in progress'
    Done = 'done'


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Status


class TaskForm(BaseModel):
    title: str
    description: Optional[str] = None
    status: Status


tasks = []


@app.get('/')
async def index():
    logger.info('Отработал GET запрос.')
    return {"message": "Task list manager"}


@app.get('/tasks', response_model=list[Task], summary='Получение списка задач')
async def get_tasks():
    logger.info('Отработал GET запрос.')
    return tasks


@app.get('/tasks/{task_id}', response_model=Task, summary='Информация о задаче по ее ID')
async def get_task(task_id: int):
    for el in tasks:
        if el.id == task_id:
            logger.info(f'Отработал DELETE запрос для task id = {task_id}.')
            return el
    raise HTTPException(status_code=404, detail='Task with this ID not found')


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

# Создать API для добавления нового пользователя в базу данных. Приложение
# должно иметь возможность принимать POST запросы с данными нового
# пользователя и сохранять их в базу данных.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте маршрут для добавления нового пользователя (метод POST).
# 📌 Реализуйте валидацию данных запроса и ответа.
import hashlib
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str


class UserForm(BaseModel):
    name: str
    email: EmailStr = Field(..., description='Email address')
    password: str = Field(..., min_length=8, regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$', description='Password')


users = []


@app.get('/')
async def root():
    logger.info('Отработал GET запрос.')
    return {"message": "User list manager"}


@app.get('/users', response_model=list[User], summary='Получение списка пользователей')
async def read_list():
    logger.info('Отработал GET запрос.')
    return users


@app.post("/users", summary='Добавить нового пользователя', tags=['Users'])
async def create_user(user: UserForm):
    new_user_id = 1
    if users:
        new_user_id = max(users, key=lambda x: x.id).id + 1
    new_user = User(id=new_user_id,
                    name=user.name,
                    email=user.email,
                    password=hashlib.md5(user.password).hexdigest())
    users.append(new_user)
    logger.info('Отработал POST запрос.')


@app.put('/users/{user_id}', response_model=User, summary='Изменение данных пользователя')
async def update_user(user_id: int, user: UserForm):
    for el in users:
        if el.id == user_id:
            el.name = user.name
            el.email = user.email
            el.password = hashlib.md5(user.password).hexdigest()
            logger.info(f'Отработал PUT запрос для user id = {user_id}.')
            return el
    raise HTTPException(status_code=404, detail='User with this ID not found')


@app.delete('/users/{user_id}', summary='Удаление пользователя')
async def delete_user(user_id: int):
    for el in users:
        if el.id == user_id:
            users.remove(el)
            logger.info(f'Отработал DELETE запрос для user id = {user_id}.')
            return
    raise HTTPException(status_code=404, detail='User with this ID not found')

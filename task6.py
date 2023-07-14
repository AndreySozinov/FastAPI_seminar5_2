"""
Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
📌 Создайте класс User с полями id, name, email и password.
📌 Создайте список users для хранения пользователей.
📌 Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
📌 Создайте маршрут для отображения списка пользователей (метод GET).
📌 Реализуйте вывод списка пользователей через шаблонизатор Jinja.
"""
import hashlib
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory='templates')


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str


class UserForm(BaseModel):
    name: str
    email: EmailStr = Field(..., description='Email address')
    password: str = Field(..., min_length=8, pattern=r'^([a-z])([A-Z])(\d).*$', description='Password')


users = []
user1 = User(id=1, name='Viktor Petrov', email='fsfs@uy.com', password='fdJJ4sdrggrs4')
user2 = User(id=2, name='Petr Viktorov', email='fsdffs@uy.com', password='ffd55ddJJ4ss4')
user3 = User(id=3, name='Anna Semenova', email='ffs@uy.com', password='fsgfgdJJ4rrgg4')
users.append(user1)
users.append(user2)
users.append(user3)


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    logger.info('Отработал GET запрос.')
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/users', response_class=HTMLResponse,
         response_model=list[User], summary='Получение списка пользователей')
async def read_list(request: Request):
    global users
    logger.info('Отработал GET запрос.')
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


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


@app.put('/users/{user_id}', response_model=User, summary='Изменение данных пользователя', tags=['Users'])
async def update_user(user_id: int, user: UserForm):
    for el in users:
        if el.id == user_id:
            el.name = user.name
            el.email = user.email
            el.password = hashlib.md5(user.password).hexdigest()
            logger.info(f'Отработал PUT запрос для user id = {user_id}.')
            return el
    raise HTTPException(status_code=404, detail='User with this ID not found')


@app.delete('/users/{user_id}', summary='Удаление пользователя', tags=['Users'])
async def delete_user(user_id: int):
    for el in users:
        if el.id == user_id:
            users.remove(el)
            logger.info(f'Отработал DELETE запрос для user id = {user_id}.')
            return
    raise HTTPException(status_code=404, detail='User with this ID not found')

# Создать API для получения списка фильмов по жанру. Приложение должно
# иметь возможность получать список фильмов по заданному жанру.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс Movie с полями id, title, description и genre.
# 📌 Создайте список movies для хранения фильмов.
# 📌 Создайте маршрут для получения списка фильмов по жанру (метод GET).
# 📌 Реализуйте валидацию данных запроса и ответа.
import logging
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class Genre(BaseModel):
    id: int
    name: str


class Movie(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genre_id: list[int]


class MovieForm(BaseModel):
    title: str
    description: Optional[str] = None
    genre_id: list[int]


genres = []
movies = []


@app.get('/')
async def index():
    logger.info('Отработал GET запрос.')
    return {"message": "Movie list manager"}


@app.get('/movies', response_model=list[Movie], summary='Получение списка фильмов, отсортированных по жанру')
async def read_list(gen_id: int = None):
    if gen_id:
        movie_list = [m for m in movies if gen_id in m.genre_id]
        logger.info('Отработал GET запрос.')
        return movie_list
    logger.info('Отработал GET запрос.')
    return movies


@app.post("/movies", response_model=Movie, summary='Добавление нового фильма')
async def create_movie(movie: MovieForm):
    new_movie_id = 1
    if movies:
        new_movie_id = max(movies, key=lambda x: x.id).id + 1
    new_movie = Movie(id=new_movie_id, title=movie.title, description=movie.description, genre_id=movie.genre_id)
    movies.append(new_movie)
    logger.info('Отработал POST запрос.')
    return new_movie


@app.put('/movies/{task_id}', response_model=Movie, summary='Изменение данных о фильме')
async def update_movie(movie_id: int, movie: MovieForm):
    for el in movies:
        if el.id == movie_id:
            el.title = movie.title
            el.description = movie.description
            el.genre_id = movie.genre_id
            logger.info(f'Отработал PUT запрос для task id = {movie_id}.')
            return el
    raise HTTPException(status_code=404, detail='Movie with this ID not found')


@app.delete('/movies/{movie_id}', summary='Удаление фильма')
async def delete_movie(movie_id: int):
    for el in movies:
        if el.id == movie_id:
            movies.remove(el)
            logger.info(f'Отработал DELETE запрос для task id = {movie_id}.')
            return
    raise HTTPException(status_code=404, detail='Movie with this ID not found')

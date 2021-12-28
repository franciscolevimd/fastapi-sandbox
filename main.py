# Python
from typing import Optional


# Pydantic
from pydantic import BaseModel


# FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query


app = FastAPI()


# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get('/')
def home():
    return {'result': 'OK'}


# Request and Response body
@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person


# Validaciones: query Parameters
@app.get('/person/detail')
def show_person(
        name: Optional[str] = Query(None, min_length=1, max_length=50),
        age: str = Query(...)
):
    return {name: age}

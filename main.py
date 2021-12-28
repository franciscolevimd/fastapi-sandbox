# Python
from typing import Optional


# Pydantic
from pydantic import BaseModel


# FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path


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


# Validaciones: Query Parameters
@app.get('/person/detail')
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title='Person Name',
            description='This is the person name. It\'s between 1 and 50 '
            'characters'
        ),
        age: str = Query(
            ...,
            title='Person Age',
            description='This is the person name. It\'s required'
        )
):
    return {name: age}


# Validaciones: Path Parameters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person Id',
        description='This is the person id. It\'s required'
    )
):
    return {person_id: 'It exists!'}

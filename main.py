# Python
from typing import Optional
from enum import Enum


# Pydantic
from pydantic import BaseModel
from pydantic import Field


# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form


app = FastAPI()


# Models
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'
    blue = 'blue'


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Arisaurio'
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Rex'
    )
    age: int = Field(
        ...,
        gt=0,
        le=1000,
        example=17
    )
    hair_color: Optional[HairColor] = Field(default=None, example='blue')
    is_married: Optional[bool] = Field(default=None, example=False)

    # class Config:
    #     schema_extra = {
    #         'example': {
    #             'first_name': 'Arisaurio',
    #             'last_name': 'Rex',
    #             'age': 17,
    #             'hair_color': 'blue',
    #             'is_married': False
    #         }
    #     }


class Person(PersonBase):
    password: str = Field(..., min_length=8)


class PersonOut(PersonBase):
    pass


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    class Config:
        schema_extra = {
            'example': {
                'city': 'Ixtapaluca',
                'state': 'México',
                'country': 'México We'
            }
        }


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example='levbono2022')
    message: str = Field(default='Login Succesfuly!')


@app.get(
    path='/',
    status_code=status.HTTP_200_OK
)
def home():
    return {'result': 'OK'}


# Request and Response body
@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters
@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK
)
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title='Person Name',
            description='This is the person name. It\'s between 1 and 50 '
            'characters',
            example='Francisco Leví'
        ),
        age: str = Query(
            ...,
            title='Person Age',
            description='This is the person name. It\'s required',
            example=36
        )
):
    return {name: age}


# Validaciones: Path Parameters
@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK
)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person Id',
        description='This is the person ID',
        example=23
    )
):
    return {person_id: 'It exists!'}


# Validaciones: Request Body
@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK
)
def update_person(
    person_id: int = Path(
        ...,
        title='PersonId',
        description='This is the person ID',
        gt=0,
        example=99
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
    # return person


@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return LoginOut(username=username)

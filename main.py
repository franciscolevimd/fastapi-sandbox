# Python
from typing import Optional
from enum import Enum


# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File


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
    status_code=status.HTTP_200_OK,
    tags=['Home'],
    summary='Main page'
)
def home():
    return {'result': 'OK'}


# Request and Response body
@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Persons'],
    summary='Create Person in the app'
)
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and saves the information
    in the database.

    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name,
        age, hair color and marital status.

    Returns a person model with first name, last name, age, hair color and
    marital status.
    """
    return person


# Validaciones: Query Parameters
@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary='Retreives the basic Person information',
    deprecated=True
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
    """
    This path operation retrieves the basic information of a person.

    Parameters:
    - Query parameters:
        - **name: str** -> Name of the person sought.
        - **age: str** -> Age of the person sought.

    Returns the name of the person with its age.
    """
    return {name: age}


# Validaciones: Path Parameters


persons = [1, 2, 3, 4, 5, 6]


@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary='Indicates whether or not a person\'s record exists'
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
    """
    This path operation returns a message indicating whether or not a person's
    record exists.

    Parameters:
    - Path parameter:
        - **person_id: int** -> Person Id.

    Returns a successful message if the Person Id exists in the database else
    an unsuccessful message.
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This person doesn\'t exist!'
        )
    return {person_id: 'It exists!'}


# Validaciones: Request Body
@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary='Updates the Person data'
)
def update_person(
    person_id: int = Path(
        ...,
        title='PersonId',
        description='This is the person ID',
        gt=0,
        example=99,
        tags=['Persons']
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    """
    This path operation updates a person data.

    Parameters:
    - Path parameter:
        - **person_id: int** -> Person Id.
    - Request body parameters:
        - **person: Person** -> A person model with first name, last name,age,
        hair color and marital status.
        - **location: Location** -> A location model with city, state and
        country.

    Returns the person data with its location data.
    """
    results = person.dict()
    results.update(location.dict())
    return results
    # return person


# Forms
@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary='Authenticate an username in the app'
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    This path operation is used to authenticate to the app.

    Parameters:
    - Form Data:
        - **username: str** -> Name with which the user has registered.
        - **password: str**


    Returns a success message if the user has registered with the application,
    otherwise an error message.
    """
    return LoginOut(username=username)


# Cookies and Headers Parametres
@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=['Contacts'],
    summary='Send a message to the app staff'
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    """
    This path operation is used to contact the staff of the app.

    Parameters:
    - Form Data:
        - **first_name: str** -> First name of the user.
        - **last_name: str** -> Last name of the user.
        - **email: EmailStr** -> Valid email address.
        - **message: str** -> Message that you want to send to the application.
        staff.
    - Header parameters:
        - **user_agent: str**
    - Cookies parameters:
        - **ads: str**
    """
    return user_agent


# Files
@app.post(
    path='/post-image',
    tags=['Images'],
    summary='Upload an image to the app'
)
def post_image(
    image: UploadFile = File(...)
):
    """
    This path operation is used to upload a imagen file

    Parameters:
    - File data:
        - **image: UploadFile** -> An image file.

    Returns the filename, its format and size.
    """
    return {
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(kb)': round(len(image.file.read()) / 1024, ndigits=2)
    }

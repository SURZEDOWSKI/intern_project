from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import json

usrList = []

class Usr:
    def __init__(self, id, country, dateOfBirth, firstName, lastName, nickname, gender, email):
        self.id = id
        self.country = country
        self.dateOfBirth = dateOfBirth
        self.firstName = firstName
        self.lastName = lastName
        self.nickname = nickname
        self.gender = gender
        self.email = email

def usrCreate(country, dateOfBirth, firstName, lastName, nickname, gender, email):
    newId=len(usrList)+1
    usrList.append(Usr(newId, country, dateOfBirth, firstName, lastName, nickname, gender, email))

def usrEdit(ID, country, dateOfBirth, firstName, lastName, nickname, gender, email):
    usrList[ID].country = country
    usrList[ID].dateOfBirth = dateOfBirth
    usrList[ID].firstName = firstName
    usrList[ID].lastName = lastName
    usrList[ID].nickname = nickname
    usrList[ID].gender = gender
    usrList[ID].email = email

def findUserById(ID):
    for x in range(len(usrList)):
        if usrList[x].id == ID:
            return x 


class User(BaseModel):
    id: int
    country: str
    dateOfBirth: str
    firstName: str
    lastName: str
    nickname: str
    gender: str
    email: str

class UserWithoutId(BaseModel):
    country: str
    dateOfBirth: str
    firstName: str
    lastName: str
    nickname: str
    gender: str
    email: str

app =FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/users/{userId}')
async def get_user(userId: int):
    x = findUserById(userId)
    return usrList[x].__dict__

@app.put('/users/{userId}', response_model=User)
async def edit_user(userId: int, user: UserWithoutId):
    x = findUserById(userId)
    y = user.__dict__
    usrEdit(x, y["country"], y["dateOfBirth"], y["firstName"], y["lastName"], y["nickname"], y["gender"], y["email"])
    msg = usrList[x]
    return msg.__dict__

@app.post('/users', response_model=User)
async def create_user(user: UserWithoutId):
    usrCreate(user.country, user.dateOfBirth, user.firstName, user.lastName, user.nickname, user.gender, user.email)
    msg = usrList[len(usrList)-1]
    return msg.__dict__

usrCreate("PL", "1999-08-06", "Szymon", "Urzedowski", "Wazon", "male", "uzi166@gmail.com")
print(len(usrList))



{
  "id": 1,
  "country": "PL",
  "dateOfBirth": "1999-08-06",
  "firstName": "Szymon",
  "lastName": "Urzedowski",
  "nickname": "Wazon",
  "gender": "male",
  "email": "uzi166@gmail.com"
}
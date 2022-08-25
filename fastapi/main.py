from email.policy import default
from typing import Union, List
from fastapi import FastAPI, status, HTTPException, Query
from pydantic import BaseModel
import json
from fastapi.responses import JSONResponse

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

def deleteUsr(ID):
    usrList.pop(ID)

def findUserById(ID):
    for x in range(len(usrList)):
        if usrList[x].id == ID:
            return x

def findUserByNickname(nickname):
    for x in range(len(usrList)):
        if usrList[x].nickname == nickname:
            return x

def findUserByEmail(email):
    for x in range(len(usrList)):
        if usrList[x].email == email:
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

class Message(BaseModel):
    message: str

app =FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/v1/users')
async def find_user(userId: List[int] | None = Query(default=None), nickname: str | None = None, email: str | None = None):
    if userId == None and nickname == None and email == None:
        if len(usrList) != 0:
            return usrList
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"There are no users!"})
    elif userId != None and nickname == None and email == None:
        foundUsrList = []
        for i in range(len(userId)):
            ID = findUserById(userId[i])
            foundUsrList.append(usrList[ID].__dict__)
        if len(foundUsrList) != 0:
            return foundUsrList
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="User not found")
    elif userId == None and nickname != None and email == None:
        ID = findUserByNickname(nickname)
        if ID:
            return usrList[ID].__dict__
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="User not found!")
    elif userId == None and nickname == None and email != None:
        ID = findUserByEmail(email)
        if ID:
            return usrList[ID].__dict__
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="User not found!")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="too many parameters passed!")
    
@app.get('/v1/users/{userId}', response_model=User, responses={status.HTTP_404_NOT_FOUND: {"model": Message}})
async def get_user(userId: int):
    ID = findUserById(userId)
    if ID != None:
        return usrList[ID].__dict__
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found!"})

@app.put('/v1/users/{userId}', response_model=User, responses={status.HTTP_404_NOT_FOUND: {"model": Message}})
async def edit_user(userId: int, user: UserWithoutId):
    ID = findUserById(userId)
    if ID != None:
        y = user.__dict__
        usrEdit(ID, y["country"], y["dateOfBirth"], y["firstName"], y["lastName"], y["nickname"], y["gender"], y["email"])
        msg = usrList[ID]
        return msg.__dict__
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found!"})

@app.delete('/v1/users/{userId}',
    responses={status.HTTP_200_OK: {"model": Message},
               status.HTTP_404_NOT_FOUND: {"model": Message}})
async def delete_user(userId: int):
    ID = findUserById(userId)
    if ID != None:
        deleteUsr(ID)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Sucessfully deleted user!"})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found!"})

@app.post('/v1/users', response_model=User, status_code=status.HTTP_200_OK)
async def create_user(user: UserWithoutId):
    usrCreate(user.country, user.dateOfBirth, user.firstName, user.lastName, user.nickname, user.gender, user.email)
    msg = usrList[len(usrList)-1]
    return msg.__dict__

usrCreate("PL", "1999-08-06", "Szymon", "Urzedowski", "Wazon", "male", "wazon@gmail.com")
usrCreate("PL", "1990-08-06", "Paweł", "Nowak", "Nowy", "male", "nowy@gmail.com")
usrCreate("PL", "1995-08-06", "Anna", "Kowalska", "Ania", "female", "ania@gmail.com")

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
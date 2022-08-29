from email.policy import default
from typing import List
from fastapi import FastAPI, status, HTTPException, Query
from pydantic import BaseModel
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
    if len(usrList) == 0:
        newId = 1
    else:
        newId = usrList[-1].id+1
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
    founfUsrlist = []
    for x in range(len(usrList)):
        if usrList[x].nickname == nickname:
            founfUsrlist.append(x)
    return founfUsrlist

def findUserByEmail(email):
    founfUsrlist = []
    for x in range(len(usrList)):
        if usrList[x].email == email:
            founfUsrlist.append(x)
    return founfUsrlist

def removeResponse(key):
    r = dict(resp)
    del r[key]
    return r

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

resp = {status.HTTP_200_OK: {},
        status.HTTP_400_BAD_REQUEST: {},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_405_METHOD_NOT_ALLOWED: {},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_503_SERVICE_UNAVAILABLE: {}}

app =FastAPI(description="Users Service is an application to manage users identities :) It allows to create, get, filter, update and delete users accounts.")

#@app.get("/")
#def read_root():
#    return {"Hello": "World"}

@app.get('/v1/users', responses=resp)
async def find_user(userId: List[int] | None = Query(default=None), nickname: str | None = None, email: str | None = None):
    if userId == None and nickname == None and email == None:
        if len(usrList) != 0:
            return usrList
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif userId != None and nickname == None and email == None:
        foundUsrList = []
        for i in range(len(userId)):
            ID = findUserById(userId[i])
            foundUsrList.append(usrList[ID].__dict__)
        if len(foundUsrList) != 0:
            return foundUsrList
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif userId == None and nickname != None and email == None:
        ID = findUserByNickname(nickname)
        if ID != None:
            foundUsrList = []
            for i in range(len(ID)):
                foundUsrList.append(usrList[ID[i]])
            return foundUsrList
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif userId == None and nickname == None and email != None:
        ID = findUserByEmail(email)
        if ID != None:
            foundUsrList = []
            for i in range(len(ID)):
                foundUsrList.append(usrList[ID[i]])
            return foundUsrList
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
@app.get('/v1/users/{userId}', response_model=User, responses=resp)
async def get_user(userId: int):
    ID = findUserById(userId)
    if ID != None:
        return usrList[ID].__dict__
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

@app.put('/v1/users/{userId}', response_model=User, responses=resp)
async def edit_user(userId: int, user: UserWithoutId):
    ID = findUserById(userId)
    if ID != None:
        y = user.__dict__
        usrEdit(ID, y["country"], y["dateOfBirth"], y["firstName"], y["lastName"], y["nickname"], y["gender"], y["email"])
        msg = usrList[ID]
        return msg.__dict__
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

@app.delete('/v1/users/{userId}', responses=resp)
async def delete_user(userId: int):
    ID = findUserById(userId)
    if ID != None:
        deleteUsr(ID)
        raise HTTPException(status.HTTP_200_OK)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.post('/v1/users', response_model=User, responses=removeResponse(status.HTTP_404_NOT_FOUND))
async def create_user(user: UserWithoutId):
    usrCreate(user.country, user.dateOfBirth, user.firstName, user.lastName, user.nickname, user.gender, user.email)
    msg = usrList[len(usrList)-1]
    return msg.__dict__

usrCreate("PL", "1999-08-06", "Szymon", "Urzedowski", "Wazon", "male", "wazon@gmail.com")
usrCreate("PL", "1990-08-06", "Paweł", "Nowak", "Nowy", "male", "nowy@gmail.com")
usrCreate("PL", "1995-08-06", "Anna", "Kowalska", "Ania", "female", "ania@gmail.com")

"""
    {
    "id": 1,
    "country": "PL",
    "dateOfBirth": "1999-08-06",
    "firstName": "Szymon",
    "lastName": "Urzedowski",
    "nickname": "Wazon",
    "gender": "male",
    "email": "uzi1662@gmail.com"
    }
"""
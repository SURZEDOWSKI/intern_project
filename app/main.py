from typing import List
from fastapi import FastAPI, status, HTTPException, Query
from pydantic import BaseModel


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


usr_list = []


class Usr:
    def __init__(
        self, id, country, dateOfBirth, firstName, lastName, nickname, gender, email
    ):
        self.id = id
        self.country = country
        self.dateOfBirth = dateOfBirth
        self.firstName = firstName
        self.lastName = lastName
        self.nickname = nickname
        self.gender = gender
        self.email = email


def usr_create(country, dateOfBirth, firstName, lastName, nickname, gender, email):
    if len(usr_list) == 0:
        new_id = 1
    else:
        new_id = usr_list[-1].id + 1
    usr_list.append(
        Usr(new_id, country, dateOfBirth, firstName, lastName, nickname, gender, email)
    )


def usr_edit(ID, country, dateOfBirth, firstName, lastName, nickname, gender, email):
    usr_list[ID].country = country
    usr_list[ID].dateOfBirth = dateOfBirth
    usr_list[ID].firstName = firstName
    usr_list[ID].lastName = lastName
    usr_list[ID].nickname = nickname
    usr_list[ID].gender = gender
    usr_list[ID].email = email


def usr_delete(ID):
    usr_list.pop(ID)


def find_usr_by_id(ID):
    for x in range(len(usr_list)):
        if usr_list[x].id == ID:
            return x


def find_usr_by_nickname(nickname):
    found_list = []
    for x in range(len(usr_list)):
        if usr_list[x].nickname.startswith(nickname):
            found_list.append(usr_list[x].__dict__)
    if len(found_list) != 0:
        return found_list


def find_usr_by_email(email):
    found_list = []
    for x in range(len(usr_list)):
        if usr_list[x].email.startswith(email):
            found_list.append(usr_list[x].__dict__)
    if len(found_list) != 0:
        return found_list


def remove_response(key):
    r = dict(resp)
    del r[key]
    return r


def num_of_params(*args):
    count = 0
    par = None
    for x in args:
        if x != None:
            count = count + 1
    return count


resp = {
    status.HTTP_200_OK: {},
    status.HTTP_400_BAD_REQUEST: {},
    status.HTTP_404_NOT_FOUND: {},
    status.HTTP_405_METHOD_NOT_ALLOWED: {},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    status.HTTP_503_SERVICE_UNAVAILABLE: {},
}

app = FastAPI(
    description="Users Service is an application to manage users identities :) It allows to create, get, filter, update and delete users accounts."
)

# @app.get("/")
# def read_root():
#    return {"Hello": "World"}


@app.get("/v1/users", responses=resp)
async def find_user(
    user_id: List[int] | None = Query(default=None),
    nickname: str | None = None,
    email: str | None = None,
):
    parameters = num_of_params(user_id, nickname, email)

    if parameters == 0:
        if len(usr_list) != 0:
            return usr_list
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif parameters == 1:
        if user_id != None:
            temp_found_usr_list = []
            for i in range(len(user_id)):
                ID = find_usr_by_id(user_id[i])
                if ID != None:
                    temp_found_usr_list.append(usr_list[ID].__dict__)
            if len(temp_found_usr_list) != 0:
                return temp_found_usr_list
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        elif nickname != None:
            user_ids_list = find_usr_by_nickname(nickname)
            if user_ids_list != None:
                return user_ids_list
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        elif email != None:
            user_ids_list = find_usr_by_email(email)
            if user_ids_list != None:
                return user_ids_list
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/v1/users/{user_id}", response_model=User, responses=resp)
async def get_user(user_id: int):
    ID = find_usr_by_id(user_id)
    if ID != None:
        return usr_list[ID].__dict__
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.put("/v1/users/{user_id}", response_model=User, responses=resp)
async def edit_user(user_id: int, user: UserWithoutId):
    ID = find_usr_by_id(user_id)
    if ID != None:
        y = user.__dict__
        usr_edit(
            ID,
            y["country"],
            y["dateOfBirth"],
            y["firstName"],
            y["lastName"],
            y["nickname"],
            y["gender"],
            y["email"],
        )
        msg = usr_list[ID]
        return msg.__dict__
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.delete("/v1/users/{user_id}", responses=resp)
async def delete_user(user_id: int):
    ID = find_usr_by_id(user_id)
    if ID != None:
        usr_delete(ID)
        raise HTTPException(status.HTTP_200_OK)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.post(
    "/v1/users",
    response_model=User,
    responses=remove_response(status.HTTP_404_NOT_FOUND),
)
async def create_user(user: UserWithoutId):
    usr_create(
        user.country,
        user.dateOfBirth,
        user.firstName,
        user.lastName,
        user.nickname,
        user.gender,
        user.email,
    )
    msg = usr_list[len(usr_list) - 1]
    return msg.__dict__


usr_create("PL", "1999-08-06", "Szymon", "Urzedowski", "Wazon", "male", "wazon@gmail.com")
usr_create("PL", "1990-08-06", "Paweł", "Nowak", "Nowy", "male", "nowy@gmail.com")
usr_create("PL", "1995-08-06", "Anna", "Kowalska", "Ania", "female", "ania@gmail.com")


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

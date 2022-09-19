from typing import List, Optional
from fastapi import FastAPI, status, HTTPException, Query
from pydantic import BaseModel

from sqlmodel import SQLModel, create_engine, Field, Session, select, delete


class UserWithoutId(SQLModel):
    country: str
    dateOfBirth: str
    firstName: str
    lastName: str
    nickname: str = Field(index=True)
    gender: str
    email: str = Field(index=True)


class User(UserWithoutId, table=True):

    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    nickname: str = Field(index=True)
    email: str = Field(index=True)


class UserRead(UserWithoutId):
    id: int


class UserUpdate(UserWithoutId):
    country: Optional[str] = None
    dateOfBirth: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    nickname: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None


connection_string = "postgresql://postgres:pass@172.18.0.2:5432/postgres"  # use Postgres:5432 to run localy


engine = create_engine(connection_string, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


def num_of_params(*args):
    count = 0
    par = None
    for x in args:
        if x != None:
            count = count + 1
    return count


def remove_response(key):
    r = dict(resp)
    del r[key]
    return r


def get_users_by_id(user_id):
    with Session(engine) as session:
        statement = "SELECT * FROM users WHERE id in ("
        statement += ", ".join(str(i) for i in user_id)
        statement += ")"
        users = session.exec(statement).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return users


def get_user_by_nickname(nickname):
    with Session(engine) as session:
        statement = "SELECT * FROM users WHERE nickname LIKE '"
        statement += nickname
        statement += "%'"
        users = session.exec(statement).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return users


def get_user_by_email(email):
    with Session(engine) as session:
        statement = "SELECT * FROM users WHERE email LIKE '"
        statement += email
        statement += "%'"
        users = session.exec(statement).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return users


def get_all_users():
    with Session(engine) as session:
        users = session.exec(statement=select(User).order_by(User.id)).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return users


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


@app.on_event("startup")
async def on_startup():
    with Session(engine) as session:
        create_tables()


@app.on_event("shutdown")
def on_shutdown():
    with Session(engine) as session:
        statement = delete(User)
        result = session.exec(statement)
        session.commit()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post(
    "/v1/users",
    response_model=UserRead,
    responses=remove_response(status.HTTP_404_NOT_FOUND),
)
async def create_user(user: UserWithoutId):
    with Session(engine) as session:
        db_user = User.from_orm(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@app.get("/v1/users/{user_id}", response_model=UserRead, responses=resp)
async def get_user(user_id: int):
    with Session(engine) as session:
        users = session.exec(statement=select(User).where(User.id == user_id)).first()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        print(users)
    return users


@app.put("/v1/users/{user_id}", response_model=UserRead, responses=resp)
async def edit_user(user_id: int, user: UserUpdate):
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@app.delete("/v1/users/{user_id}", responses=resp)
async def delete_user(user_id: int):
    with Session(engine) as session:
        users = session.exec(statement=select(User).where(User.id == user_id)).first()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        session.delete(users)
        session.commit()
        raise HTTPException(status.HTTP_200_OK)


@app.get("/v1/users", responses=resp)
async def find_user(
    user_id: List[int] | None = Query(default=None),
    nickname: str | None = None,
    email: str | None = None,
):
    parameters = num_of_params(user_id, nickname, email)
    if parameters == 0:
        users = get_all_users()
        return users
    elif parameters == 1:
        if user_id != None:
            users = get_users_by_id(user_id)
            return users
        elif nickname != None:
            users = get_user_by_nickname(nickname)
            return users
        elif email != None:
            users = get_user_by_email(email)
            return users
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

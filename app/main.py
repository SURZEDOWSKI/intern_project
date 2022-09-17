from typing import List, Optional
from fastapi import FastAPI, status, HTTPException, Query
from pydantic import BaseModel

from sqlmodel import SQLModel, create_engine, Field, Session, select, delete


class User(SQLModel, table=True):

    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    country: str
    dateOfBirth: str
    firstName: str
    lastName: str
    nickname: str = Field(index=True)
    gender: str
    email: str = Field(index=True)

class UserWithoutId(SQLModel):
    country: str
    dateOfBirth: str
    firstName: str
    lastName: str
    nickname: str
    gender: str
    email: str

class UserRead(SQLModel):
    id: int
    country: str
    dateOfBirth: str
    firstName: str
    lastName: str
    nickname: str
    gender: str
    email: str


#connection_string = "postgresql://postgres:pass@Postgres:5432/postgres"
connection_string = "postgresql://postgres:pass@docker:5432/postgres"

engine = create_engine(connection_string, echo=True)

print(engine)

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


def create_users():
    user_1 = User(country="PL", dateOfBirth="1999.08.06", firstName="Szymon", lastName="Urzedowski", nickname="Wazon", gender="male", email="szymon@gmail.com")
    user_2 = User(country="US", dateOfBirth="1990.08.10", firstName="John", lastName="Smith", nickname="Jonny", gender="male", email="john@gmail.com")
    user_3 = User(country="UK", dateOfBirth="2000.08.19", firstName="Scott", lastName="Looker", nickname="Scotty", gender="male", email="scott@gmail.com")

    with Session(engine) as session:

        session.add(user_1)
        session.add(user_2)
        session.add(user_3)

        session.commit()


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
        #statement = delete(User)
        #result = session.exec(statement)
        #session.commit()
        create_tables()
        #users = session.exec(statement = select(User).where(User.id==1)).first()
        #if users == None:
        #    create_users()


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
        users = session.exec(statement = select(User).where(User.id==user_id)).first()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        print(users)
    return users


@app.put("/v1/users/{user_id}", response_model=UserRead, responses=resp)
async def edit_user(user_id: int, user: UserWithoutId):
    with Session(engine) as session:
        users = session.exec(statement = select(User).where(User.id==user_id)).first()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        print(users)

        users.country = user.country
        users.dateOfBirth = user.dateOfBirth
        users.firstName = user.firstName
        users.lastName = user.lastName
        users.nickname = user.nickname
        users.gender = user.gender
        users.email = user.email

        session.add(users)
        session.commit()
        session.refresh(users)
    return users


@app.delete("/v1/users/{user_id}", responses=resp)
async def delete_user(user_id: int):
    with Session(engine) as session:
        users = session.exec(statement = select(User).where(User.id==user_id)).first()
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
    with Session(engine) as session:
        parameters = num_of_params(user_id, nickname, email)
        if parameters == 0:
            users = session.exec(statement = select(User).order_by(User.id)).all()
            if not users:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return users
        elif parameters == 1:
            if user_id != None:
                statement = "SELECT * FROM users WHERE id in ("
                statement +=', '.join(str(i) for i in user_id)
                statement += ")"
                users = session.exec(statement).all()
                if not users:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
                return users
            elif nickname != None:
                statement = "SELECT * FROM users WHERE nickname LIKE '"
                statement += nickname
                statement += "%'"
                users = session.exec(statement).all()
                if not users:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
                return users
            elif email != None:
                statement = "SELECT * FROM users WHERE email LIKE '"
                statement += email
                statement += "%'"
                users = session.exec(statement).all()
                if not users:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
                return users
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
               

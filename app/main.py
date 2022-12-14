from typing import List, Optional
from fastapi import (
    FastAPI,
    status,
    HTTPException,
    Query,
    Request,
    Response,
    BackgroundTasks,
)
from fastapi.encoders import jsonable_encoder
from fastapi_redis_cache import FastApiRedisCache, cache
from pydantic import BaseModel
import redis
import json
import aio_pika
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


class UserEvent(BaseModel):
    action_type: str
    user: dict


POSTGRES_CONNECTION_STRING = "postgresql://postgres:pass@Postgres:5432/postgres"

REDIS_CONNECTION_STRING = "redis://Redis:6379"

engine = create_engine(POSTGRES_CONNECTION_STRING, echo=True)

r = redis.Redis(host="Redis", port="6379")


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
        users = session.exec(statement=select(User).where(User.id.in_(user_id))).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        users = jsonable_encoder(users)
        return users


def get_user_by_nickname(nickname):
    with Session(engine) as session:
        users = session.exec(
            statement=select(User).where(User.nickname == nickname)
        ).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        users = jsonable_encoder(users)
        return users


def get_user_by_email(email):
    with Session(engine) as session:
        users = session.exec(statement=select(User).where(User.email == email)).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        users = jsonable_encoder(users)
        return users


def get_all_users():
    with Session(engine) as session:
        users = session.exec(statement=select(User).order_by(User.id)).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        users = jsonable_encoder(users)
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


async def publish_message(msg):
    connection = await aio_pika.connect("amqp://guest:guest@Rabbitmq")

    async with connection:
        q_name = "users_queue"

        channel = await connection.channel()
        await channel.declare_queue(q_name, auto_delete=True)

        message = aio_pika.Message(body=json.dumps(msg.dict()).encode())
        await channel.default_exchange.publish(message, routing_key=q_name)


@app.on_event("startup")
async def on_startup():
    with Session(engine) as session:
        create_tables()
    cache = FastApiRedisCache()
    cache.init(
        host_url=REDIS_CONNECTION_STRING,
        prefix="cache",
        response_header="X-Cache",
        ignore_arg_types=[Request, Response, Session],
    )


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
async def create_user(user: UserWithoutId, bg_tasks: BackgroundTasks):
    with Session(engine) as session:
        db_user = User.from_orm(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        keys = r.keys("*")
        if keys:
            r.delete(*keys)

    user_event = UserEvent(action_type="user created", user=db_user.dict())
    bg_tasks.add_task(publish_message, user_event)

    return db_user


@app.get("/v1/users/{user_id}", response_model=UserRead, responses=resp)
@cache(expire=30)
async def get_user(user_id: int, response: Response):
    with Session(engine) as session:
        users = session.get(User, user_id)
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        users = jsonable_encoder(users)
        print(r.get(f"cache:main.get_user(user_id={user_id})"))
        return users


@app.put("/v1/users/{user_id}", response_model=UserRead, responses=resp)
async def edit_user(user_id: int, user: UserUpdate, bg_tasks: BackgroundTasks):
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

        keys_none = r.keys(f"*user_id=None, nickname=None, email=None*")
        keys_by_id = r.keys(f"*user_id=*{db_user.id}*")
        keys_by_nickname = r.keys(f"*nickname={db_user.nickname}*")
        keys_by_email = r.keys(f"*email={db_user.email}*")
        keys = keys_none + keys_by_id + keys_by_nickname + keys_by_email

        if keys:
            r.delete(*keys)

    user_event = UserEvent(action_type="user edited", user=db_user.dict())
    bg_tasks.add_task(publish_message, user_event)

    return db_user


@app.delete("/v1/users/{user_id}", responses=resp)
async def delete_user(user_id: int, bg_tasks: BackgroundTasks):
    with Session(engine) as session:
        users = session.exec(statement=select(User).where(User.id == user_id)).first()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        session.delete(users)
        session.commit()

        keys_none = r.keys(f"*user_id=None, nickname=None, email=None*")
        keys_by_id = r.keys(f"*user_id=*{users.id}*")
        keys_by_nickname = r.keys(f"*nickname={users.nickname}*")
        keys_by_email = r.keys(f"*email={users.email}*")
        keys = keys_none + keys_by_id + keys_by_nickname + keys_by_email

        if keys:
            r.delete(*keys)

    print(users.dict())
    user_event = UserEvent(action_type="user deleted", user=users.dict())
    bg_tasks.add_task(publish_message, user_event)
    print(users.dict())

    return HTTPException(status.HTTP_200_OK)


@app.get("/v1/users", responses=resp)
@cache(expire=30)
async def find_user(
    response: Response,
    user_id: List[int] | None = Query(default=None),
    nickname: str | None = Query(default=None),
    email: str | None = Query(default=None),
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

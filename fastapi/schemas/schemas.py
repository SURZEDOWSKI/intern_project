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

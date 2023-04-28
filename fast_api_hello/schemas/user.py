from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: int


class UpdateUser(BaseModel):
    name: str
    email: str
    password: str


class RegUser(BaseModel):
    name: str
    email: str
    password: str
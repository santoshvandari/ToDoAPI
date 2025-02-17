from pydantic import BaseModel
from Model.schema import DisplayTask


class CreateUser(BaseModel):
    email: str
    password: str

class UserData(BaseModel):
    id: int
    email: str
    tasklist: list[DisplayTask]


class Token(BaseModel):
    access_token: str
    token_type: str

class Register(Token):
    email: str
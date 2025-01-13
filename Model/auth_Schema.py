from pydantic import BaseModel

class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    username: str

class UserInDB(BaseModel):
    username: str

class UserData(BaseModel):
    username: str
    email: str
    todos: list = []


class CreateUser(BaseModel):
    username: str
    email: str
    password: str
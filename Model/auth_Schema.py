from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    password: str

class UserData(BaseModel):
    id: int
    email: str
    tasklist: list

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None

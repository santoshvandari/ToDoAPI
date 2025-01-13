from typing import Optional
from pydantic import BaseModel

class CreateTask(BaseModel):
    title: str
    description: str
    status: bool = False

class UpdateTask(BaseModel):
    title: str = None
    description: str = None
    status: bool = None

class DisplayTask(BaseModel):
    id: int
    title: str
    description: str
    status: bool


class CreateUser(BaseModel):
    username: str
    email: str
    password: str
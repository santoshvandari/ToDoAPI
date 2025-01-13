from pydantic import BaseModel

class CreateTask(BaseModel):
    title: str
    description: str
    status: bool = False


class DisplayTask(BaseModel):
    id: int
    title: str
    description: str
    status: bool

    # class Config:
    #     orm_mode = True
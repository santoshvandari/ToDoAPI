from pydantic import BaseModel, ConfigDict

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
    userid: int

    model_config = ConfigDict(from_orm=True)

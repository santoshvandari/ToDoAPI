from fastapi import APIRouter
from DB.getdb import get_db
from Model.schema import CreateTask, DisplayTask
from sqlalchemy.orm import Session
from fastapi import Depends
from DB.model import ToDo

route=APIRouter()

@route.get("/")
async def read_root():
    db = get_db()

    return {"Hello": "World"}


@route.post("/create")
def create_task(task: CreateTask, db: Session = Depends(get_db)):
    todo=ToDo(title=task.title,description=task.description,status=task.status)
    print(todo)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return task


@route.get("/task",response_model=list[DisplayTask])
def get_task(db: Session = Depends(get_db)):
    tasklist= db.query(ToDo).all()
    print(tasklist)
    return tasklist

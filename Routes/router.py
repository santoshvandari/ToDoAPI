from fastapi import APIRouter
from DB.getdb import get_db
from Model.schema import CreateTask, DisplayTask,UpdateTask
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


@route.get("/task/{id}",response_model=DisplayTask)
def get_single_task(id:int,db: Session = Depends(get_db)):
    task=db.query(ToDo).filter(ToDo.id==id).first()
    return task



@route.patch("/task/{id}")
def update_task(id:int,task:UpdateTask,db:Session=Depends(get_db)):
    data = task.dict(exclude_unset=True)
    if not data :
        return {"message":"No data to update"}
    todo=db.query(ToDo).filter(ToDo.id==id).first()
    if not todo:
        return {"message":"Task not found"}
    for key,value in data.items():
        if value==None or value=="":
            continue
        setattr(todo,key,value)
    db.commit()
    db.refresh(todo)
    return {"message":"Updated", "data":data}

@route.delete("/task/{id}")
def delete_task(id:int,db:Session=Depends(get_db)):
    todo=db.query(ToDo).filter(ToDo.id==id)
    todo.delete(synchronize_session=False)
    db.commit()
    return {"message":"Task Deleted"}



from fastapi import APIRouter, HTTPException,status
from DB.db_config import get_db
from Model.schema import CreateTask, DisplayTask,UpdateTask
from sqlalchemy.orm import Session
from fastapi import Depends
from DB.model import ToDo
from Auth.utillity import get_current_user

route=APIRouter(tags=["Task"])
# route = APIRouter()

@route.get("/")
async def read_root():
    # db = get_db()
    return {"Hello": "World"}


@route.post("/create")
def create_task(task: CreateTask, db: Session = Depends(get_db),user=Depends(get_current_user)):
    todo=ToDo(title=task.title,description=task.description,status=task.status,userid=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)



@route.get("/task")
async def get_task(db: Session = Depends(get_db),user=Depends(get_current_user)):
    tasklist= await  db.query(ToDo).filter(ToDo.userid==user.id).all()
    return tasklist


@route.get("/task/{id}",response_model=DisplayTask)
async def get_single_task(id:int,db: Session = Depends(get_db),user=Depends(get_current_user)):
    task=db.query(ToDo).filter(ToDo.id==id & ToDo.userid==user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="Task not found")
    return task



@route.patch("/task/{id}")
async def update_task(id:int,task:UpdateTask,db:Session=Depends(get_db),user=Depends(get_current_user)):
    data = task.dict(exclude_unset=True)
    if not data :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,details="No data provided")  
    todo=db.query(ToDo).filter(ToDo.id==id & ToDo.userid==user.id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="Task not found")
    for key,value in data.items():
        if value==None or value=="":
            continue
        setattr(todo,key,value)
    db.commit()
    db.refresh(todo)
    return {"message":"Updated", "data":data}

@route.delete("/task/{id}")
async def delete_task(id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    todo=db.query(ToDo).filter(ToDo.id==id & ToDo.userid==user.id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="Task not found")
    db.delete(todo)
    db.commit()
    return {"message":"Task deleted Successfyully"}





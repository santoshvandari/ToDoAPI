from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from Auth.utillity import authenticate_user,create_access_token, get_current_user,get_password_hash
from DB.db_config import get_db
from DB.model import ToDo,User
from sqlalchemy.orm import Session
from Model.auth_Schema import Token,CreateUser,UserData,Register
from Model.schema import DisplayTask


authroute = APIRouter(tags=["Auth"])

@authroute.get("/auth")
async def read_root():
    return {"Hello": "World"}


@authroute.post("/token",response_model=Token)
async def login_for_access_token(from_data:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    user= authenticate_user(db,from_data.username,from_data.password)
    if not user:
        raise HTTPException(status_code=400,detail="Incorrect username or password")
    access_token= create_access_token(user.id,user.email)
    return Token(access_token=access_token,token_type="bearer")


@authroute.post("/register",response_model=Register)
async def create_user(user:CreateUser,db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==user.email).first():
        raise HTTPException(status_code=400,detail="User already exists")
    db_user=User(email=user.email,password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token= create_access_token(db_user.id,db_user.email)
    return Register(access_token=access_token,token_type="bearer",email=db_user.email)
    


@authroute.get("/users/me",response_model=UserData)
async def read_users_me(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    print(current_user)
    userid= current_user.id
    tasklist= db.query(ToDo).filter(ToDo.userid==userid).all()
    tasks=[DisplayTask.model_validate(task.__dict__) for task in tasklist]
    return UserData(id=current_user.id,email=current_user.email,tasklist=tasks)
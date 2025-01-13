from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from DB.getdb import get_db
from Model.auth_Schema import Token, CreateUser, UserData
from Auth.utility import authenticate_user, create_access_token, get_current_user, get_current_active_user, get_password_hash
from Auth.utility import ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session
from DB.model import User,ToDo



# to get a string like this run:







authroute = APIRouter()




@authroute.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@authroute.post("/createuser")
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user= User(username=user.username,email=user.email,password=get_password_hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    # get the token 
    accesstoken = create_access_token(data={"sub": user.username})
    return {"access_token": accesstoken, "token_type": "bearer", "user": user}



@authroute.get("/users/me", response_model=UserData)
async def read_users_me(current_user: Annotated[UserData, Depends(get_current_active_user)], db: Session = Depends(get_db)):

    tasklist = db.query(ToDo).filter(ToDo.userid==current_user.id).all()
    return {"username": current_user.username, "email": current_user.email, "todos": tasklist}

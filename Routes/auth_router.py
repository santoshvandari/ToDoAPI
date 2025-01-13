from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from DB.getdb import get_db
from Model.auth_Schema import Token, TokenData, User, UserInDB
from Auth.utility import authenticate_user, create_access_token, get_current_user, get_current_active_user
from Auth.utility import ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session



# to get a string like this run:







authroute = APIRouter()




@authroute.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@authroute.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@authroute.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@authroute.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}
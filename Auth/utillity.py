from datetime import datetime, timedelta
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from DB.model import User
from passlib.context import CryptContext
import jwt,os
from DB.db_config import get_db
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


print()

# bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password,hashed_password):
    return bcrypt_context.verify(plain_password,hashed_password)


def get_password_hash(password):
    return bcrypt_context.hash(password)


def create_access_token(id,email):
    to_encode={"id":id,"email":email}
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db:Session,email:str,password:str):
    user=db.query(User).filter(User.email==email).first()
    if not user:
        return False
    if not verify_password(password,user.password):
        return False
    return user


def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user=db.query(User).filter(User.email==email).first()
    if user is None:
        raise credentials_exception
    return user
from Routes.router import route
from Routes.auth_router import authroute
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from DB.model import Base
from DB.db_config import engine
import os



if not os.path.exists("todo.db"):
    Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(route)
app.include_router(authroute)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow all origins OR you can add your frontend url here
    allow_credentials=True,
    allow_methods=["GET", "POST","PATCH","DELETE"],
    allow_headers=["*"],
)


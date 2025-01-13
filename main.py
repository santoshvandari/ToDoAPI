from Routes.router import route
from fastapi import FastAPI
from DB.model import Base
from DB.db_config import engine
import os



if not os.path.exists("todo.db"):
    Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(route)


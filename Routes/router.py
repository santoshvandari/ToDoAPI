from fastapi import APIRouter
from DB.getdb import get_db

route=APIRouter()

@route.get("/")
async def read_root():
    db = get_db()

    return {"Hello": "World"}
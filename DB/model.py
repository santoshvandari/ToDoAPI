from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean


Base = declarative_base()

class ToDo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(Boolean)


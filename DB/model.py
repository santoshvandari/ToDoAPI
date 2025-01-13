from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()

class ToDo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    status = Column(Boolean,default=False)
    userid=Column(Integer,ForeignKey('user.id'))
    user  = relationship("User", back_populates="todo")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    username = Column(String,unique=True,index=True,nullable=False)
    email = Column(String,unique=True,index=True,nullable=False)
    password = Column(String,nullable=False)
    todo = relationship("ToDo", back_populates="user")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Database configuration
DATABASE_URL = "sqlite:///todo.db"

engine=create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)


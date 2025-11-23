import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

url = os.getenv("DATABASE_URL")

engine = create_engine(url, echo=True)

Base = declarative_base()

def init_db():
    import model
    Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
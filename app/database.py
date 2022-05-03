from curses import flash
from venv import create
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PSQL_USER = 'postgress'
PSQL_USER_PASSWORD = 'toor1234'
HOST_NAME = 'localhost'
DB_NAME = 'fastapi'


SQLALCHEMY_DATABASE_URL = 'postgresql://kiruthik:toor1234@localhost/fastapi'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{PSQL_USER}:{PSQL_USER_PASSWORD}/{HOST_NAME}/{DB_NAME}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor

PSQL_USER = 'postgress'
PSQL_USER_PASSWORD = 'toor1234'
HOST_NAME = 'localhost'
DB_NAME = 'fastapi'


# SQLALCHEMY_DATABASE_URL = 'postgresql://kiruthik:toor1234@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
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

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='kiruthik', password='toor1234', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed!")
#         print("Error: ", error)
#         time.sleep(2)
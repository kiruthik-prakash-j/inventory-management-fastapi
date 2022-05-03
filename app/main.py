from random import randrange
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from . import schemas
from . import utils

ROW_SIZE = 5
COLUMN_SIZE = 6


models.Base.metadata.create_all(bind=engine)


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='kiruthik', password='toor1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesful!")
        break
    except Exception as error:
        print("Connecting to database failed!")
        print("Error: ", error)
        time.sleep(2)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello WOrld!"}


@app.get("/items", response_model=List[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items


@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=schemas.ItemResponse)
def create_items(item: schemas.ItemDB, db: Session = Depends(get_db)):
    # new_item = models.Item(item_name=item.name, quantity=item.quantity, row_no=ROW_NO, column_no=COLUMN_NO, is_empty=False)
    new_item = models.Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/items/{id}", response_model=schemas.ItemResponse)
def get_item(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    # print(item)
    if not item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"message with id: {id} does not exist")
    return item


@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id)
    if item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"item with id: {id} does not exist")
    
    item.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/items/{id}", response_model=schemas.ItemResponse)
def update_item(id: int, updated_item : schemas.ItemDB,  db: Session = Depends(get_db)):
    item_query = db.query(models.Item).filter(models.Item.id == id)
    item = item_query.first()
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {id} does not exits")
    
    item_query.update(updated_item.dict(), synchronize_session=False)
    db.commit()
    return item_query.first()


@app.post("/reset",  status_code=status.HTTP_201_CREATED)
def reset_table(db: Session = Depends(get_db)):
    for row_no in range (0, ROW_SIZE):
        for col_no in range (0, COLUMN_SIZE):
            new_item = models.Item(item_name='NA', quantity=0, row_no=row_no, column_no=col_no, is_empty=True)
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
    
    return {"message": "reset successful"}


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {id} does not exits")
    return user

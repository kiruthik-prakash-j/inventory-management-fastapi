from random import randrange
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


class Item(BaseModel):
    name: str
    quantity: int


class ItemDB(BaseModel):
    item_name: str
    quantity: int
    row_no: int
    column_no: int
    is_empty: bool = True

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


my_items = [
    {
        "name": "apples",
        "quantity": 1,
        "id": 1
    },
    {
        "name": "mango",
        "quantity": 3,
        "id": 2
    }
]

def find_item(id):
    for item in my_items:
        if item['id'] == id:
            return item


def find_item_index(id):
    for index, item in enumerate(my_items):
        if item["id"] == id:
            return index


@app.get("/")
async def root():
    return {"message": "Hello WOrld!"}


@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    # select_query = """ SELECT * FROM items"""
    # cursor.execute(select_query)
    # items = cursor.fetchall()
    # print(items)
    items = db.query(models.Item).all()
    return {"items": items}


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_items(item: ItemDB, db: Session = Depends(get_db)):
    # print(item.dict())
    # item_dict = item.dict()
    # item_dict['id'] = randrange(0, 100000)
    # my_items.append(item_dict)
    # insert_query = """ INSERT INTO items (item_name, quantity, row_no, column_no) VALUES (%s, %s, %s, %s) RETURNING *"""
    # record = (item.name, item.quantity, 0, 3)
    # cursor.execute(insert_query, record)
    # new_item = cursor.fetchone()
    # conn.commit()
    # new_item = models.Item(item_name=item.name, quantity=item.quantity, row_no=ROW_NO, column_no=COLUMN_NO, is_empty=False)
    new_item = models.Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"new_item": new_item}




@app.get("/items/{id}")
def get_item(id: int, db: Session = Depends(get_db)):
    # item = find_item(id)
    # select_query = """ SELECT * FROM items WHERE id = %s"""
    # record = (str(id))
    # cursor.execute(select_query,record)
    # item = cursor.fetchone()
    item = db.query(models.Item).filter(models.Item.id == id).first()
    # print(item)
    if not item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"message with id: {id} does not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"item with id: {id} was not found"}
    return {"item": item}


@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db)):
    # item_index = find_item_index(id)
    # if not item_index:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"item with id: {id} does not exist")
    # my_items.pop(item_index)
    # delete_query = """ DELETE FROM items WHERE id = %s RETURNING *"""
    # record = (str(id))
    # cursor.execute(delete_query,record)
    # deleted_item = cursor.fetchone()
    # conn.commit()
    item = db.query(models.Item).filter(models.Item.id == id)
    if item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"item with id: {id} does not exist")
    
    item.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/items/{id}")
def update_item(id: int, updated_item : ItemDB,  db: Session = Depends(get_db)):
    # item_index = find_item_index(id)
    # if item_index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"Item with id {id} does not exits")
    # item_dict = item.dict()
    # item_dict["id"] = id
    # my_items[item_index] = item_dict


    # row_number = 0
    # column_number = 0
    # update_query = """ UPDATE items SET item_name = %s, quantity = %s, row_no = %s, column_no = %s WHERE id = %s RETURNING *"""
    # record = (item.name, item.quantity, row_number, column_number, str(id))
    # cursor.execute(update_query, record)
    # updated_item = cursor.fetchone()
    # conn.commit()

    item_query = db.query(models.Item).filter(models.Item.id == id)
    item = item_query.first()
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {id} does not exits")
    
    item_query.update(updated_item.dict(), synchronize_session=False)
    db.commit()
    return {"data": item_query.first()}

@app.get("/sqlalchemy")
def test_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return {"data: ":items}
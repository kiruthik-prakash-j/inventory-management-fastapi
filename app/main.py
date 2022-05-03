from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Item(BaseModel):
    name: str
    quantity: int

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Toor@1234', cursor_factory=RealDictCursor)
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
def get_items():
    select_query = """ SELECT * FROM items"""
    cursor.execute(select_query)
    items = cursor.fetchall()
    # print(items)
    return {"items": items}


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_items(item: Item):
    # print(item.dict())
    # item_dict = item.dict()
    # item_dict['id'] = randrange(0, 100000)
    # my_items.append(item_dict)
    ROW_NO = 0
    COLUMN_NO = 0
    insert_query = """ INSERT INTO items (item_name, quantity, row_no, column_no) VALUES (%s, %s, %s, %s) RETURNING *"""
    record = (item.name, item.quantity, 0, 3)
    cursor.execute(insert_query, record)
    new_item = cursor.fetchone()
    conn.commit()
    return {"new_item": f"name : {item.name}, quantity : {item.quantity}"}




@app.get("/items/{id}")
def get_item(id: int):
    # item = find_item(id)
    select_query = """ SELECT * FROM items WHERE id = %s"""
    record = (str(id))
    cursor.execute(select_query,record)
    item = cursor.fetchone()
    print(item)
    if not item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"message with id: {id} does not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"item with id: {id} was not found"}
    return {"item": item}


@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int):
    # item_index = find_item_index(id)
    # if not item_index:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"item with id: {id} does not exist")
    # my_items.pop(item_index)
    delete_query = """ DELETE FROM items WHERE id = %s RRETURNING *"""
    record = (str(id))
    cursor.execute(delete_query,record)
    deleted_item = cursor.fetchone()
    conn.commit()
    if not deleted_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"item with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/items/{id}")
def update_item(id: int, item : Item):
    # item_index = find_item_index(id)
    # if item_index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"Item with id {id} does not exits")
    # item_dict = item.dict()
    # item_dict["id"] = id
    # my_items[item_index] = item_dict
    row_number = 0
    column_number = 0
    update_query = """ UPDATE items SET item_name = %s, quantity = %s, row_no = %s, column_no = %s WHERE id = %s RETURNING *"""
    record = (item.name, item.quantity, row_number, column_number, str(id))
    cursor.execute(update_query, record)
    updated_item = cursor.fetchone()
    conn.commit()
    if updated_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {id} does not exits")
    return {"data": updated_item}
from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    quantity: int

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
    return {"items": my_items}


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_items(item: Item):
    print(item.dict())
    item_dict = item.dict()
    item_dict['id'] = randrange(0, 100000)
    my_items.append(item_dict)
    return {"new_item": f"name : {item.name}, quantity : {item.quantity}"}


@app.get("/items/{id}")
def get_item(id: int):
    item = find_item(id)
    if not item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"message with id: {id} does not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"item with id: {id} was not found"}
    return {"item": item}


@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int):
    item_index = find_item_index(id)
    if not item_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"item with id: {id} does not exist")
    my_items.pop(item_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/items/{id}")
def update_item(id: int, item : Item):
    item_index = find_item_index(id)
    if item_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {id} does not exits")
    item_dict = item.dict()
    item_dict["id"] = id
    my_items[item_index] = item_dict
    return {"messag": f"Item with id {id} has been updated"}
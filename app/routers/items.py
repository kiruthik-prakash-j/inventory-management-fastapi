from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

ROW_SIZE = 5
COLUMN_SIZE = 6

router = APIRouter(
    prefix="/items",
    tags=['Items']
)

@router.get("/", response_model=List[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # print(limit)
    items = db.query(models.Item).filter(models.Item.item_name.contains(search)).limit(limit).offset(skip).all()
    return items


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ItemResponse)
def create_items(item: schemas.ItemDB, db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    # new_item = models.Item(item_name=item.name, quantity=item.quantity, row_no=ROW_NO, column_no=COLUMN_NO, is_empty=False)
    # print(user.email)
    new_item = models.Item(owner_id=current_user.id ,**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.post("/reset",  status_code=status.HTTP_201_CREATED)
def reset_table(db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    for row_no in range (0, ROW_SIZE):
        for col_no in range (0, COLUMN_SIZE):
            new_item = models.Item(item_name='NA', quantity=0, row_no=row_no, column_no=col_no, is_empty=True, owner_id=current_user.id)
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
    
    return {"message": "reset successful"}


@router.get("/{id}", response_model=schemas.ItemResponse)
def get_item(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    # print(item)
    if not item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"message with id: {id} does not exist")
    return item


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    item_query = db.query(models.Item).filter(models.Item.id == id)
    item = item_query.first()
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"item with id: {id} does not exist")
    
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Not Authorized to perform the requested action!")

    item_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.ItemResponse)
def update_item(id: int, updated_item : schemas.ItemDB,  db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    item_query = db.query(models.Item).filter(models.Item.id == id)
    item = item_query.first()
    if item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {id} does not exits")
    
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Not Authorized to perform the requested action!")

    item_query.update(updated_item.dict(), synchronize_session=False)
    db.commit()
    return item_query.first()




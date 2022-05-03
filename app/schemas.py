from pydantic import BaseModel, EmailStr
from datetime import datetime

class ItemBase(BaseModel):
    item_name: str
    quantity: int


class ItemDB(ItemBase):
    row_no: int
    column_no: int
    is_empty: bool = True

class ItemResponse(BaseModel):
    item_name: str
    quantity: int
    row_no: int
    column_no: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
import email
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


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
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

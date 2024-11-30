# Define Pydantic schemas for request validation and responses.

from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class ExpenseCreate(BaseModel):
    category: str
    amount: float
    description: Optional[str] = None


class ExpenseResponse(BaseModel):
    id: int
    category: str
    amount: float
    description: Optional[str]

    class Config:
        orm_mode = True

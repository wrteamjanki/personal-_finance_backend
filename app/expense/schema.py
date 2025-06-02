from pydantic import BaseModel
from datetime import date
from typing import Optional

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: date
    note: Optional[str] = ""

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[date] = None
    note: Optional[str] = ""

class ExpenseEntry(BaseModel):
    id: int
    amount: float
    category: str
    date: date
    note: Optional[str] = ""

    class Config:
        from_attributes = True

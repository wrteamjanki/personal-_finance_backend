from pydantic import BaseModel
from datetime import date
from typing import Optional

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: date
    note: Optional[str] = ""

class ExpenseUpdate(BaseModel):
    amount: Optional[float]
    category: Optional[str]
    date: Optional[date]
    note: Optional[str] = ""

class ExpenseEntry(ExpenseCreate):
    id: int

    class Config:
        from_attributes = True

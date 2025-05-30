from pydantic import BaseModel
from datetime import date
from typing import Optional

class IncomeBase(BaseModel):
    amount: float
    category: str
    date: date
    note: Optional[str] = ""

class IncomeCreate(IncomeBase):
    amount: float
    category: str
    date: date
    note: Optional[str] = ""

class IncomeUpdate(BaseModel):
    amount: Optional[float]
    category: Optional[str]
    date: Optional[date]
    note: Optional[str]

class IncomeEntry(IncomeBase):
    id: int

    class Config:
        from_attributes = True

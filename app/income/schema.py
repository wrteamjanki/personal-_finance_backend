from pydantic import BaseModel
from datetime import date
from typing import Optional

# class IncomeBase(BaseModel):
#     amount: float
#     category: str
#     date: date
#     note: Optional[str] = ""
class IncomeCreate(BaseModel):
    amount: float
    category: str
    date: date
    note: Optional[str] = "" # Or Optional[str] = "" if you want empty string as default

class IncomeUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[date] = None
    note: Optional[str] = ""

class IncomeEntry(BaseModel):
    id: int
    amount: float
    category: str
    date: date
    note: Optional[str] = None

    class Config:
        from_attributes = True

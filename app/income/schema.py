from pydantic import BaseModel
import datetime
from typing import Optional

class IncomeBase(BaseModel):
    amount: float
    category: str
    date: datetime.date  # ✅ updated
    note: Optional[str] = ""

class IncomeCreate(BaseModel):
    amount: float
    category: str
    date: datetime.date  # ✅ updated
    note: Optional[str] = ""

class IncomeUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[datetime.date] = None  # ✅ updated
    note: Optional[str] = ""

class IncomeEntry(BaseModel):
    id: int
    amount: float
    category: str
    date: datetime.date  # ✅ updated
    note: Optional[str] = None

    class Config:
        from_attributes = True

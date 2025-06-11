from pydantic import BaseModel
from typing import Optional
import datetime

class SavingBase(BaseModel):
    amount: float
    category: str
    date: datetime.date
    note: Optional[str] = ""
    title: str

class SavingCreate(SavingBase):
    amount: float
    category: str
    date: datetime.date
    note: Optional[str] = ""
    title: str

class SavingUpdate(SavingBase):
    pass

class SavingEntry(SavingBase):
    id: int

    class Config:
        from_attributes = True

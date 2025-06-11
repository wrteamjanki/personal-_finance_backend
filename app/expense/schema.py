from pydantic import BaseModel,ConfigDict
import datetime
from typing import Optional

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: datetime.date
    note: Optional[str] = ""

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[datetime.date] = None
    note: Optional[str] = ""
    
class ExpenseEntry(BaseModel):
    id: int
    amount: float
    category: str
    date: Optional[datetime.date] = None
    note: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

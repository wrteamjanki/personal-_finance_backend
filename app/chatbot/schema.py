from pydantic import BaseModel
from datetime import date
from typing import Literal

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    type: Literal["expense", "income"]
    amount: float
    category: str
    date: date
    note: str
    confirmation: str

# app/api/chatbot/schemas.py

from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    intent: str
    amount: float | None = None
    category: str | None = None
    date: str | None = None
    note: str | None = None
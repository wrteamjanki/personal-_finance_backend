from pydantic import BaseModel
from typing import List, Optional
from datetime import date
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    intent: str
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[str] = None
    note: Optional[str] = None
    reply: Optional[str] = None

class ChatResponseList(BaseModel):
    responses: List[ChatResponse]

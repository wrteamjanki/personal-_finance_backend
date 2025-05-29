from fastapi import APIRouter, Depends
from app.chatbot.schema import ChatRequest, ChatResponse
from app.chatbot.service import handle_chat
from app.auth.router import oauth2_scheme

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, token: str = Depends(oauth2_scheme)):
    return await handle_chat(request.message)

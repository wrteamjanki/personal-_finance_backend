from fastapi import APIRouter
from app.chatbot.schema import ChatRequest, ChatResponse
from app.chatbot.service import handle_chat

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return await handle_chat(request.message)

from fastapi import APIRouter
from app.chatbot.service import handle_chat
from app.chatbot.schema import ChatRequest, ChatResponseList

router = APIRouter()

@router.post("/chat", response_model=ChatResponseList)
async def chat_handler(request: ChatRequest):
    return await handle_chat(request.message)

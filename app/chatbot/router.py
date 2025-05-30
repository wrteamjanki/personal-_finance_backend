from fastapi import APIRouter
from app.chatbot.service import handle_chat
# from app.auth.dependencies import get_current_user
from app.chatbot.schema import ChatRequest, ChatResponse, ChatResponseList

router = APIRouter()

@router.post("/chat", response_model=ChatResponseList)
async def chat_handler(request: ChatRequest):
    return await handle_chat(request.message)

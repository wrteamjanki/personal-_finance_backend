# app/chatbot/router.py

from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user, User
from app.chatbot.service import handle_chat
from app.chatbot.schema import ChatRequest, ChatResponseList

router = APIRouter(
    prefix="/api/chatbot",
    tags=["Chatbot"]
)

@router.post("/chat", response_model=ChatResponseList)
async def chat_handler(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    return await handle_chat(request.message)
print("✅ Chatbot router loaded")

from fastapi import APIRouter
from app.chatbot.service import handle_chat
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, token: str = Depends(get_current_user)):
    return await handle_chat(request.message)

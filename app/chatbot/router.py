from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import get_current_user
from app.db.models import User as UserModel  # ✅ fix
from app.chatbot.service import handle_chat
from app.chatbot.schema import ChatRequest, ChatResponseList
from app.db.database import get_async_session

router = APIRouter(
    prefix="/api/chatbot",
    tags=["Chatbot"]
)

@router.post("/chat", response_model=ChatResponseList)
async def chat_handler(
    request: ChatRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user)  # ✅ use UserModel here
):
    return await handle_chat(request.message, db, current_user.id)

print("✅ Chatbot router loaded")

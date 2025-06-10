from fastapi import APIRouter
from app.chatbot.routes import router as chat_routes

router = APIRouter()
router.include_router(chat_routes, prefix="/chat", tags=["Chat"])
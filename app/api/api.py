from fastapi import APIRouter
from app.api.v1.endpoints import auth, chat_completion, expense, income  # add more as needed

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(chat_completion.router)
api_router.include_router(expense.router)
api_router.include_router(income.router)  # future

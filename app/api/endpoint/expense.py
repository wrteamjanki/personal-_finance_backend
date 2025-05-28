from fastapi import APIRouter
from app.expense.routes import router as expense_routes

router = APIRouter()
router.include_router(expense_routes, prefix="/expense", tags=["Expense"])

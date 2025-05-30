from fastapi import APIRouter
from app.income.routes import router as income_routes

router = APIRouter()
router.include_router(income_routes, prefix="/income", tags=["Income"])
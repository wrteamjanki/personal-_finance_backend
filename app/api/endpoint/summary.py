from fastapi import APIRouter
from app.summary.schema import router as summary_router

router = APIRouter()
router.include_router(summary_router, prefix="/summary", tags=["Summary"])
from fastapi import APIRouter
from app.saving.router import router as saving_routes

router = APIRouter()
router.savin_router(income_routes, prefix="/saving", tags=["Saving"])
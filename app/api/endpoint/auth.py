from fastapi import APIRouter
from app.auth.routes import router as auth_routes

router = APIRouter()
router.include_router(auth_routes, prefix="/auth", tags=["Auth"])

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.auth.dependencies import get_current_user
from app.db.models import User
from app.summary.service import get_summary
from app.summary.schema import SummaryResponse

router = APIRouter(prefix="/summary", tags=["summary"])

@router.get("/savings", response_model=SummaryResponse)
async def summary_savings(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    return await get_summary(db, current_user.id)

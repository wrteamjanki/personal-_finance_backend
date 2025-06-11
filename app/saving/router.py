from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.saving.schema import SavingCreate, SavingEntry, SavingUpdate
from app.saving import service
from app.db.database import get_async_session
from app.auth.dependencies import get_current_user
from app.db.models import User

router = APIRouter(prefix="/saving", tags=["Saving"])

@router.post("/", response_model=SavingEntry)
async def add_saving(entry: SavingCreate, db: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    return await service.add_saving(db, entry, current_user.id)

@router.get("/", response_model=List[SavingEntry])
async def get_savings(db: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    return await service.get_all_savings(db, current_user.id)

@router.put("/{saving_id}", response_model=SavingEntry)
async def update_saving(saving_id: int, entry: SavingUpdate, db: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    updated = await service.update_saving(db, saving_id, entry, current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Saving not found")
    return updated

@router.delete("/{saving_id}")
async def delete_saving(saving_id: int, db: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    deleted = await service.delete_saving(db, saving_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Saving not found")
    return {"detail": "Saving deleted successfully"}

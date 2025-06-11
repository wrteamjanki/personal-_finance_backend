from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.saving.schema import SavingCreate, SavingUpdate
from app.db.models import Saving
from typing import List

async def add_saving(db: AsyncSession, entry: SavingCreate, user_id: int) -> Saving:
    new_saving = Saving(**entry.dict(), user_id=user_id)
    db.add(new_saving)
    await db.commit()
    await db.refresh(new_saving)
    return new_saving

async def get_all_savings(db: AsyncSession, user_id: int):
    result = await db.execute(select(Saving).where(Saving.user_id == user_id))
    return result.scalars().all()

async def update_saving(db: AsyncSession, saving_id: int, entry: SavingUpdate, user_id: int):
    result = await db.execute(select(Saving).where(Saving.id == saving_id, Saving.user_id == user_id))
    saving = result.scalar_one_or_none()
    if not saving:
        return None
    for field, value in entry.dict().items():
        setattr(saving, field, value)
    await db.commit()
    await db.refresh(saving)
    return saving

async def delete_saving(db: AsyncSession, saving_id: int, user_id: int) -> bool:
    result = await db.execute(select(Saving).where(Saving.id == saving_id, Saving.user_id == user_id))
    saving = result.scalar_one_or_none()
    if not saving:
        return False
    await db.delete(saving)
    await db.commit()
    return True

async def add_savings_bulk(db: AsyncSession, entries: List[SavingCreate], user_id: int):
    new_savings = [Saving(**entry.dict(), user_id=user_id) for entry in entries]
    db.add_all(new_savings)
    await db.commit()
    for saving in new_savings:
        await db.refresh(saving)
    return new_savings
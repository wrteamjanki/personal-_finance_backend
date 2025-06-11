from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends
from app.db.database import get_async_session
from app.income.schema import IncomeCreate, IncomeUpdate, IncomeEntry
from app.db.models import Income



async def add_income(user_id, db: AsyncSession, entry: IncomeCreate) -> Income:
    new_income = Income(**entry.dict(), user_id=user_id)
    db.add(new_income)
    await db.commit()
    await db.refresh(new_income)
    return new_income

async def get_all_income(session: AsyncSession, user_id: int) -> List[IncomeEntry]:
    result = await session.execute(select(Income).where(Income.user_id == user_id))
    incomes = result.scalars().all()
    return [IncomeEntry.model_validate(inc) for inc in incomes]

async def delete_income(income_id: int, session: AsyncSession) -> bool:
    result = await session.execute(select(Income).where(Income.id == income_id))
    income = result.scalar_one_or_none()
    if not income:
        return False
    await session.delete(income)
    await session.commit()
    return True
async def update_income(expense_id: int, entry: IncomeUpdate, session: AsyncSession) -> IncomeEntry:
    result = await session.execute(select(Income).where(Income.id == expense_id))
    income = result.scalar_one_or_none()
    if not income:
        raise ValueError("Income entry not found")

    for key, value in entry.dict(exclude_unset=True).items():
        setattr(income, key, value)
    session.add(income)
    await session.commit()
    await session.refresh(income)
    return IncomeEntry.model_validate(income)

async def get_income_categories(db: AsyncSession,session: AsyncSession) -> List[str]:
    result = await db.execute(select(Income.category))
    categories = result.scalars().all()
    return list(set(categories))

async def add_incomes_bulk(db: AsyncSession, entries: List[IncomeCreate],user_id: int):
    new_incomes = [Income(**entry.dict(),user_id=user_id) for entry in entries]
    db.add_all(new_incomes)
    await db.commit()
    for income in new_incomes:
        await db.refresh(income)
    return new_incomes

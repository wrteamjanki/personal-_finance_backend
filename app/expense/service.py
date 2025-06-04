from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from fastapi import Depends
from app.db.database import get_async_session
from app.expense.schema import ExpenseCreate, ExpenseUpdate, ExpenseEntry
from app.db import models

async def add_expense(db: AsyncSession, user_id: int):
    new_expense = models.Expense(**entry.dict())
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return new_expense


async def get_all_expenses(session: AsyncSession = Depends(get_async_session)) -> List[ExpenseEntry]:
    result = await session.execute(select(Expence.user_id == user_id))
    expenses = result.scalars().all()
    return [ExpenseEntry.from_orm(exp) for exp in expenses]


async def delete_expense(expense_id: int, session: AsyncSession = Depends(get_async_session)) -> bool:
    result = await session.execute(select(models.Expense).where(models.Expense.id == expense_id))
    expense = result.scalar_one_or_none()
    if not expense:
        return False
    await session.delete(expense)
    await session.commit()
    return True


async def update_expense(expense_id: int, data: ExpenseUpdate, session: AsyncSession = Depends(get_async_session)) -> ExpenseEntry:
    result = await session.execute(select(models.Expense).where(models.Expense.id == expense_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise ValueError("Expense not found.")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(expense, key, value)

    session.add(expense)
    await session.commit()
    await session.refresh(expense)
    return ExpenseEntry.from_orm(expense)

async def get_categories(session: AsyncSession = Depends(get_async_session)) -> List[str]:
    result = await session.execute(select(models.Expense.category))
    categories = result.scalars().all()
    return list(set(categories))

async def add_expenses_bulk(db: AsyncSession, entries: List[ExpenseCreate]):
    new_expenses = [models.Expense(**entry.dict()) for entry in entries]
    db.add_all(new_expenses)
    await db.commit()
    for expense in new_expenses:
        await db.refresh(expense)
    return new_expenses
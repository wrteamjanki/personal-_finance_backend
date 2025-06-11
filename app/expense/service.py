from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.expense.schema import ExpenseCreate, ExpenseUpdate, ExpenseEntry
from app.db.models import Expense


async def add_expense(user_id: int, db: AsyncSession, entry: ExpenseCreate) -> Expense:
    new_expense = Expense(**entry.dict(), user_id=user_id)
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return new_expense


async def get_all_expenses(db: AsyncSession, user_id: int) -> List[ExpenseEntry]:
    result = await db.execute(select(Expense).where(Expense.user_id == user_id))
    expenses = result.scalars().all()
    return [ExpenseEntry.from_orm(exp) for exp in expenses]


async def delete_expense(user_id: int, db: AsyncSession, expense_id: int) -> bool:
    result = await db.execute(select(Expense).where(Expense.id == expense_id).where(Expense.user_id == user_id))
    expense = result.scalar_one_or_none()
    if not expense:
        return False
    await db.delete(expense)
    await db.commit()
    return True

async def update_expense(db: AsyncSession, user_id: int, expense_id: int, data: ExpenseUpdate): 
    result = await db.execute(select(Expense).where(Expense.id == expense_id).where(Expense.user_id == user_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise ValueError("Expense not found or does not belong to the user.") # Added user context to error message

    for key, value in data.dict(exclude_unset=True).items():
        setattr(expense, key, value)

    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return ExpenseEntry.from_orm(expense)

async def get_categories(db: AsyncSession) -> List[str]:
    result = await db.execute(select(Expense.category))
    categories = result.scalars().all()
    return list(set(categories))


async def add_expenses_bulk(db: AsyncSession, entries: List[ExpenseCreate],user_id: int):
    new_expenses = [Expense(**entry.dict(), user_id=user_id) for entry in entries]
    db.add_all(new_expenses)
    await db.commit()
    for expense in new_expenses:
        await db.refresh(expense)
    return new_expenses

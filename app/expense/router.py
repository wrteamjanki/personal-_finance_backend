from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.expense.schema import ExpenseCreate, ExpenseUpdate, ExpenseEntry
from app.expense import service
from app.db.database import get_async_session
from . import service
from app.db.models import Expense
router = APIRouter(prefix="/expense", tags=["expense"])

@router.post("/", response_model=ExpenseEntry)
async def add_expense(entry: ExpenseCreate, db: AsyncSession = Depends(get_async_session)):
    new_expense = await service.add_expense(db, entry)
    return new_expense

@router.get("/", response_model=List[ExpenseEntry])
async def get_expenses(db: AsyncSession = Depends(get_async_session)):
    expenses = await service.get_all_expenses(db)
    return expenses

@router.delete("/{expense_id}", response_model=dict)
async def delete_expense(expense_id: int, db: AsyncSession = Depends(get_async_session)):
    deleted = await service.delete_expense(db, expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"detail": "Expense deleted successfully"}

@router.put("/{expense_id}", response_model=ExpenseEntry)
async def update_expense(expense_id: int, data: ExpenseUpdate, db: AsyncSession = Depends(get_async_session)):
    try:
        updated_expense = await service.update_expense(db, expense_id, data)
        return updated_expense
    except ValueError:
        raise HTTPException(status_code=404, detail="Expense not found")

@router.get("/categories/", response_model=List[str])
async def get_categories(db: AsyncSession = Depends(get_async_session)):
    categories = await service.get_categories(db)
    return categories

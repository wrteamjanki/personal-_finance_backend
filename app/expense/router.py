from fastapi import APIRouter, HTTPException, Depends
from typing import List,Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.expense.schema import ExpenseCreate, ExpenseUpdate, ExpenseEntry
from app.expense import service
from app.db.database import get_async_session
from app.auth.dependencies import get_current_user
from app.db.models import Expense, User  # Optional for typing

router = APIRouter(prefix="/expense", tags=["expense"])

@router.post("/", response_model=ExpenseEntry)
async def add_expense(
    entry: ExpenseCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)):
    # Corrected order: user_id, db, entry
    new_expense = await service.add_expense(current_user.id, db, entry)
    return new_expense

@router.get("/", response_model=List[ExpenseEntry])
async def get_expenses(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    # Corrected arguments: db, user_id
    # Assuming 'user.id' was a typo and meant 'current_user.id'
    # Also, the service function get_all_expenses expects (db, user_id)
    expenses = await service.get_all_expenses(db, current_user.id)
    return expenses

@router.delete("/{expense_id}", response_model=dict)
async def delete_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    # Corrected order: user_id, db, expense_id
    deleted = await service.delete_expense(current_user.id, db, expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"detail": "Expense deleted successfully"}

@router.put("/{expense_id}", response_model=ExpenseEntry)
async def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    try:
        # Corrected order of arguments!
        updated_expense = await service.update_expense(db, current_user.id, expense_id, data)
        return updated_expense
    except ValueError as e: # Catch the specific ValueError from service
        raise HTTPException(status_code=404, detail=str(e)) # Pass the actual error message raise HTTPException(status_code=404, detail="Expense not found")

@router.get("/categories/", response_model=List[str])
async def get_categories(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user) # current_user might be unused here if service doesn't need it
):
    # This call seems correct based on service.get_categories(db)
    categories = await service.get_categories(db)
    return categories

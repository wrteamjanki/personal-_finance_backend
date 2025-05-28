from fastapi import APIRouter, HTTPException
from typing import List
from app.expense.schema import ExpenseCreate, ExpenseUpdate, ExpenseEntry
from app.expense import service

router = APIRouter(prefix="/expense", tags=["expense"])

@router.post("/", response_model=ExpenseEntry)
async def add_expense(entry: ExpenseCreate):
    new_expense = await service.add_expense(entry)
    return new_expense

@router.get("/", response_model=List[ExpenseEntry])
async def get_expenses():
    expenses = await service.get_all_expenses()
    return expenses

@router.delete("/{expense_id}", response_model=dict)
async def delete_expense(expense_id: int):
    deleted = await service.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"detail": "Expense deleted successfully"}

@router.put("/{expense_id}", response_model=ExpenseEntry)
async def update_expense(expense_id: int, data: ExpenseUpdate):
    try:
        updated_expense = await service.update_expense(expense_id, data)
        return updated_expense
    except ValueError:
        raise HTTPException(status_code=404, detail="Expense not found")

@router.get("/categories/", response_model=List[str])
async def get_categories():
    categories = await service.get_categories()
    return categories

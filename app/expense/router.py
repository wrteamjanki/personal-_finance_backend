from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.expense.schema import ExpenseCreate, ExpenseUpdate, ExpenseEntry
from app.expense import service
<<<<<<< HEAD
=======
from app.auth.dependencies import get_current_user 
>>>>>>> 58f2f395c5250be0b665bc36d0f6748b7045e8b2

router = APIRouter(prefix="/expense", tags=["expense"])

@router.post("/", response_model=ExpenseEntry)
<<<<<<< HEAD
async def add_expense(entry: ExpenseCreate):
=======
async def add_expense(entry: ExpenseCreate, token: str = Depends(get_current_user)):
>>>>>>> 58f2f395c5250be0b665bc36d0f6748b7045e8b2
    new_expense = await service.add_expense(entry)
    return new_expense

@router.get("/", response_model=List[ExpenseEntry])
<<<<<<< HEAD
async def get_expenses():
=======
async def get_expenses(token: str = Depends(get_current_user)):
>>>>>>> 58f2f395c5250be0b665bc36d0f6748b7045e8b2
    expenses = await service.get_all_expenses()
    return expenses

@router.delete("/{expense_id}", response_model=dict)
<<<<<<< HEAD
async def delete_expense(expense_id: int):
=======
async def delete_expense(expense_id: int, token: str = Depends(get_current_user)):
>>>>>>> 58f2f395c5250be0b665bc36d0f6748b7045e8b2
    deleted = await service.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"detail": "Expense deleted successfully"}

@router.put("/{expense_id}", response_model=ExpenseEntry)
<<<<<<< HEAD
async def update_expense(expense_id: int, data: ExpenseUpdate):
=======
async def update_expense(expense_id: int, data: ExpenseUpdate, token: str = Depends(get_current_user)):
>>>>>>> 58f2f395c5250be0b665bc36d0f6748b7045e8b2
    try:
        updated_expense = await service.update_expense(expense_id, data)
        return updated_expense
    except ValueError:
        raise HTTPException(status_code=404, detail="Expense not found")

@router.get("/categories/", response_model=List[str])
<<<<<<< HEAD
async def get_categories():
=======
async def get_categories(token: str = Depends(get_current_user)):
>>>>>>> 58f2f395c5250be0b665bc36d0f6748b7045e8b2
    categories = await service.get_categories()
    return categories

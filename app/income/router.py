from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.income.schema import IncomeCreate, IncomeUpdate, IncomeEntry
from app.db.database import get_async_session
from . import service
from app.db.models import Income, User
from app.auth.dependencies import get_current_user  # 💥 Un-commented

router = APIRouter(prefix="/income", tags=["Income"])

@router.post("/", response_model=IncomeEntry)
async def create_income(
    entry: IncomeCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    new_income = await service.add_income(current_user.id, db, entry)  # Correct order: user_id, db, entry
    return new_income

@router.get("/", response_model=List[IncomeEntry])
async def read_all_income(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    incomes = await service.get_all_income(db, current_user.id)  # Correct order: db, user_id
    return incomes

@router.delete("/{income_id}", response_model=dict)
async def remove_income(
    income_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user)
):
    success = await service.delete_income(income_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Income entry not found")
    return {"detail": "Income deleted successfully"}

@router.put("/{income_id}", response_model=IncomeEntry)
async def edit_income(
    income_id: int,
    entry: IncomeUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    try:
        update_income = await service.update_income(income_id, entry, db)
        return update_income
    except ValueError:
        raise HTTPException(status_code=404, detail="Income entry not found")

@router.get("/categories", response_model=List[str])
async def income_categories(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    categories = await service.get_income_categories(db, current_user.id)
    return categories

# 🔒 Optional: bulk add can be moved to a protected route in future
async def add_incomes_bulk(
    db: AsyncSession,
    entries: List[IncomeCreate]
):
    new_incomes = [Income(**entry.dict(), user_id=user_id) for entry in entries]
    db.add_all(new_incomes)
    await db.commit()
    for income in new_incomes:
        await db.refresh(income)
    return new_incomes
# from fastapi import APIRouter, HTTPException, Depends
# from typing import List
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.income.schema import IncomeCreate, IncomeUpdate, IncomeEntry
# from app.db.database import get_async_session
# from . import service
# from app.db.models import Income, User
# from app.auth.dependencies import get_current_user  # 💥 Un-commented

# router = APIRouter(prefix="/income", tags=["Income"])


# @router.post("/", response_model=IncomeEntry)
# async def create_income(
#     entry: IncomeCreate,
#     db: AsyncSession = Depends(get_async_session),
#     current_user: User = Depends(get_current_user),
# ):
#     new_income = await service.add_income(current_user.id, db, entry)  # Correct order: user_id, db, entry
#     return new_income


# @router.get("/", response_model=List[IncomeEntry])
# async def read_all_income(
#     db: AsyncSession = Depends(get_async_session),
#     current_user: User = Depends(get_current_user),
# ):
#     incomes = await service.get_all_income(db, current_user.id)  # Correct order: db, user_id
#     return incomes


# @router.delete("/{income_id}", response_model=dict)
# async def remove_income(
#     income_id: int,
#     db: AsyncSession = Depends(get_async_session),
#     current_user: User = Depends(get_current_user),
# ):
#     success = await service.delete_income(current_user.id, db, income_id)  # Correct order: user_id, db, income_id
#     if not success:
#         raise HTTPException(status_code=404, detail="Income entry not found")
#     return {"detail": "Income deleted successfully"}


# @router.put("/{income_id}", response_model=IncomeEntry)
# async def edit_income(
#     income_id: int,
#     entry: IncomeUpdate,
#     db: AsyncSession = Depends(get_async_session),
#     current_user: User = Depends(get_current_user),
# ):
#     try:
#         updated_income = await service.update_income(db, current_user.id, income_id, entry)  # Correct order: db, user_id, income_id, entry
#         return updated_income
#     except ValueError as e:  # Catch the ValueError from the service
#         raise HTTPException(status_code=404, detail=str(e))  # Include the error message


# @router.get("/categories", response_model=List[str])
# async def income_categories(
#     db: AsyncSession = Depends(get_async_session),
#     current_user: User = Depends(get_current_user),
# ):
#     categories = await service.get_income_categories(db, current_user.id)  # Correct order: db, user_id
#     return categories


# # 🔒 Optional: bulk add can be moved to a protected route in future
# @router.post("/bulk/", response_model=List[IncomeEntry])  # Added a route for bulk add
# async def add_incomes_bulk(
#     entries: List[IncomeCreate],
#     db: AsyncSession = Depends(get_async_session),
#     current_user: User = Depends(get_current_user),
# ):
#     new_incomes = await service.add_incomes_bulk(current_user.id, db, entries)  # Correct order: user_id, db, entries
#     return new_incomes
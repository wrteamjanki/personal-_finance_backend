from fastapi import APIRouter, HTTPException, Depends

from typing import List

from app.income.schema import IncomeCreate, IncomeUpdate, IncomeEntry

from app.income.service import (
    add_income,
    get_all_income,
    delete_income,
    update_income,
    get_income_categories,
)

from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/income", tags=["Income"])


@router.post("/", response_model=IncomeEntry)

async def create_income(entry: IncomeCreate, token: str = Depends(get_current_user)):

    return await add_income(entry)


@router.get("/", response_model=List[IncomeEntry])

async def read_all_income(token: str = Depends(get_current_user)):

    return await get_all_income()


@router.delete("/{income_id}", response_model=dict)

async def remove_income(income_id: int, token: str = Depends(get_current_user)):

    success = await delete_income(income_id)

    if not success:

        raise HTTPException(status_code=404, detail="Income entry not found")

    return {"detail": "Income deleted successfully"}


@router.put("/{income_id}", response_model=IncomeEntry)

async def edit_income(income_id: int, entry: IncomeUpdate, token: str = Depends(get_current_user)):
    try:

        return await update_income(income_id, entry)

    except ValueError:

        raise HTTPException(status_code=404, detail="Income entry not found")


@router.get("/categories", response_model=List[str])

async def income_categories(token: str = Depends(get_current_user)):

    return await get_income_categories()


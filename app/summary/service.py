from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.models import Income, Expense, Saving
from app.summary.schema import SummaryResponse

async def get_summary(db: AsyncSession, user_id: int) -> SummaryResponse:
    # --- Total Income & Category Breakdown ---
    income_result = await db.execute(
        select(Income.category, func.sum(Income.amount))
        .where(Income.user_id == user_id)
        .group_by(Income.category)
    )
    income_data = income_result.all()
    total_income = sum(amount for _, amount in income_data)
    income_breakdown = {category: amount for category, amount in income_data}

    # --- Total Expense & Category Breakdown ---
    expense_result = await db.execute(
        select(Expense.category, func.sum(Expense.amount))
        .where(Expense.user_id == user_id)
        .group_by(Expense.category)
    )
    expense_data = expense_result.all()
    total_expense = sum(amount for _, amount in expense_data)
    expense_breakdown = {category: amount for category, amount in expense_data}
    #----- total savings & breakdown -----
    saving_result = await db.execute(
        select(Saving.category, func.sum(Saving.amount))
        .where(Saving.user_id == user_id)
        .group_by(Saving.category)
    )
    saving_data = saving_result.all()
    total_savings = sum(amount for _, amount in saving_data)
    saving_breakdown = {category: amount for category, amount in saving_data}
    # --- Summary Calculations ---
    # savings = total_income - total_expense
    # highest_income_category = max(income_data, key=lambda x: x[1], default=(None, 0))[0]
    # most_spent_category = max(expense_data, key=lambda x: x[1], default=(None, 0))[0]
    # most_saving_category = max(saving_data, key=lambda x: x[1], default=(None, 0))[0]
    remaining = total_income - total_expense - total_savings
    return SummaryResponse(
    total_income=total_income,
    total_expense=total_expense,
    total_savings=total_savings,
    remaining_savings=remaining,  # ✅ Fix
    income_breakdown=income_breakdown,
    expense_breakdown=expense_breakdown,
    saving_breakdown=saving_breakdown   
    )


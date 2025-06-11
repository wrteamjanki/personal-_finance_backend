from typing import Dict
from pydantic import BaseModel

class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    total_savings: float
    remaining_savings: float
    income_breakdown: Dict[str, float]   # ✅ Corrected
    expense_breakdown: Dict[str, float]  # ✅ Corrected
    saving_breakdown: Dict[str, float]  # ✅ Corrected

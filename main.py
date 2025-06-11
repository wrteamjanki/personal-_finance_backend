# Load existing data or initialize
# df_expense = pd.read_csv(EXPENSE_FILE) if os.path.exists(EXPENSE_FILE) else pd.DataFrame(columns=["amount", "category", "date", "note"])
# df_income = pd.read_csv(INCOME_FILE) if os.path.exists(INCOME_FILE) else pd.DataFrame(columns=["amount", "category", "date", "note"])
# # 🧠 Function to Parse Entries Using Gemini 1.5 Pro
# def parse_entry(text):
#     today = datetime.today().strftime('%Y-%m-%d')
#     prompt = f"""
# You are a smart finance assistant. Extract all incomes and expenses from the following user message:
# "{text}"
# Return a JSON array. Each entry must have:
# - "amount" (float),
# - "category" (string),
# - "type" ("income" or "expense"),
# - "date" (YYYY-MM-DD) – use "{today}" if not provided
# - "note" (short note, or repeat the category if unclear)
# Only return a valid JSON list like:
# [
#   {{"amount": 5000, "category": "salary", "type": "income", "date": "2025-05-20", "note": "monthly salary"}},
#   {{"amount": 1200, "category": "food", "type": "expense", "date": "2025-05-20", "note": "lunch"}}
# ]
# No extra text, explanation, or formatting.
# """
#     response = model.generate_content(prompt)
#     try:
#         return json.loads(response.text.strip())
#     except Exception as e:
#         raise ValueError("⚠️ Could not parse Gemini response:\n" + str(e))

from fastapi import FastAPI, Depends, APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.expense.router import router as expense_router
from app.income.router import router as income_router
from app.chatbot.router import router as chat_router
from app.summary.router import router as summary_router
from app.saving.router import router as saving_router
from app.db.database import engine, Base, get_async_session, AsyncSession
from app.db.models import Expense, Income, User
from init_db import init_db
from app.auth.router import router as auth_router
from app.auth.dependencies import get_current_user, User
app = FastAPI(
    title="Personal Finance Bot API",
    version="1.0"
)

# 👇 Include routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(expense_router)
app.include_router(income_router)
app.include_router(saving_router)
app.include_router(summary_router)
print("Routes:")
for route in app.routes:
    print(route.path)

@app.get("/test-secure")
async def test_secure(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.email}"}
# 👇 Inject global Bearer Auth to Swagger UI
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title=app.title,
#         version=app.version,
#         description="API for managing personal finance.",
#         routes=app.routes,
#     )
#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT"
#         }
#     }
#     for path in openapi_schema["paths"].values():
#         for method in path.values():
#             method.setdefault("security", [{"BearerAuth": []}])
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Backend APIs for the Quiz Platform",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
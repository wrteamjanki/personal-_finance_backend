from app.expense.schema import ExpenseCreate
from app.expense.service import add_expenses_bulk
from app.income.schema import IncomeCreate
from app.income.service import add_incomes_bulk
from app.chatbot.schema import ChatResponse, ChatResponseList
from app.db.database import get_async_session
from datetime import datetime
import json, re, os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def build_prompt(user_message: str) -> str:
    return f"""
You are a smart and structured personal finance assistant in an app.

Your task is to understand the user's intent and extract the following fields in proper JSON format.

Always respond **only** with a JSON array of objects — each object must represent a single transaction.

---

User message:
"{user_message}"

---

Valid intents:
- add_expense
- add_income
- delete_expense
- get_summary
- get_expense_by_category
- get_income_summary

---

Example Output (for multiple intents):
[
  {{
    "intent": "add_expense",
    "amount": 500,
    "category": "food",
    "note": "banana",
    "date": "2025-05-30"
  }},
  {{
    "intent": "add_expense",
    "amount": 600,
    "category": "clothing",
    "note": "clothes",
    "date": "2025-05-30"
  }},
  {{
    "intent": "add_income",
    "amount": 500,
    "category": "savings",
    "note": "saved money",
    "date": "2025-05-30"
  }}
]

If some values are not mentioned, omit them instead of guessing.
Respond with valid fields only.
"""



async def handle_chat(user_message: str) -> ChatResponseList:
    prompt = build_prompt(user_message)
    response = model.generate_content(prompt)
    text = response.text.strip()

    print("🧠 Gemini raw response:", text)
    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        data = json.loads(cleaned)
        if not isinstance(data, list):
            data = [data]
    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", e)
        return ChatResponseList(responses=[
            ChatResponse(intent="error", note="Failed to parse model response as JSON.")
        ])

    print("✅ Parsed JSON:", data)

    expense_entries = []
    income_entries = []
    fallbacks = []

    for entry in data:
        if "date" not in entry:
            entry["date"] = datetime.now().strftime("%Y-%m-%d")

        intent = entry.get("intent", "unknown").lower().strip()

        if intent == "add_expense" and "amount" in entry and "category" in entry:
            expense_entries.append(ExpenseCreate(
                amount=entry["amount"],
                category=entry["category"],
                date=datetime.strptime(entry["date"], "%Y-%m-%d").date(),
                note=entry.get("note", "")
            ))
        elif intent == "add_income" and "amount" in entry and "category" in entry:
            income_entries.append(IncomeCreate(
                amount=entry["amount"],
                category=entry["category"],
                date=datetime.strptime(entry["date"], "%Y-%m-%d").date(),
                note=entry.get("note", "")
            ))
        else:
            fallbacks.append(ChatResponse(
                intent=intent,
                amount=entry.get("amount"),
                category=entry.get("category"),
                date=entry.get("date"),
                note=entry.get("note", "Skipped due to missing data")
            ))

    responses = []

    # ✅ Fix here
    async for db in get_async_session():
        if expense_entries:
            stored_expenses = await add_expenses_bulk(db, expense_entries)
            responses.extend(ChatResponse(
                intent="add_expense",
                amount=exp.amount,
                category=exp.category,
                date=exp.date.strftime("%Y-%m-%d"),
                note=exp.note
            ) for exp in stored_expenses)

        if income_entries:
            stored_incomes = await add_incomes_bulk(db, income_entries)
            responses.extend(ChatResponse(
                intent="add_income",
                amount=inc.amount,
                category=inc.category,
                date=inc.date.strftime("%Y-%m-%d"),
                note=inc.note
            ) for inc in stored_incomes)

    responses.extend(fallbacks)
    return ChatResponseList(responses=responses)
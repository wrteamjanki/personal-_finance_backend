from app.expense.schema import ExpenseCreate
from app.expense.service import add_expense
from app.income.schema import IncomeCreate
from app.income.service import add_income
from app.chatbot.schema import ChatResponse, ChatResponseList
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

    responses = []

    for entry in data:
        if "date" not in entry:
            entry["date"] = datetime.now().strftime("%Y-%m-%d")

        intent = entry.get("intent", "unknown").lower().strip()
        print("🚨 Intent detected:", intent)

        if intent == "add_expense" and "amount" in entry and "category" in entry:
            expense = ExpenseCreate(
                amount=entry["amount"],
                category=entry["category"],
                date=datetime.strptime(entry["date"], "%Y-%m-%d").date(),
                note=entry.get("note", "")
            )
            print("💾 Storing expense entry:", expense.dict())
            stored = await add_expense(expense)
            responses.append(ChatResponse(
                intent=intent,
                amount=stored.amount,
                category=stored.category,
                date=stored.date.strftime("%Y-%m-%d"),
                note=stored.note
            ))

        elif intent == "add_income" and "amount" in entry and "category" in entry:
            income = IncomeCreate(
                amount=entry["amount"],
                category=entry["category"],
                date=datetime.strptime(entry["date"], "%Y-%m-%d").date(),
                note=entry.get("note", "")
            )
            print("💾 Storing income entry:", income.dict())
            stored = await add_income(income)
            responses.append(ChatResponse(
                intent=intent,
                amount=stored.amount,
                category=stored.category,
                date=stored.date.strftime("%Y-%m-%d"),
                note=stored.note
            ))

        else:
            print("⚠️ Skipping invalid entry:", entry)
            responses.append(ChatResponse(
                intent=intent,
                amount=entry.get("amount"),
                category=entry.get("category"),
                date=entry.get("date"),
                note=entry.get("note", "Skipped due to missing data")
            ))

    return ChatResponseList(responses=responses)

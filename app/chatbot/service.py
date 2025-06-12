# from app.expense.schema import ExpenseCreate
from app.expense.service import add_expenses_bulk
from app.expense.schema import ExpenseCreate
from app.income.schema import IncomeCreate
from app.income.service import add_incomes_bulk
from app.saving.schema import SavingCreate
from app.saving.service import add_savings_bulk
from app.chatbot.schema import ChatResponse, ChatResponseList
from datetime import datetime
import json, re, os
import google.generativeai as genai
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from app.summary.service import get_summary

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def build_prompt(user_message: str) -> str:
    return f"""
You are a personal finance assistant.

Your job is to extract structured information from casual user messages. Respond only with a JSON array of objects.

---

Each object must include:
- "intent": one of ["add_expense", "add_income", "add_saving", "get_summary", "small_talk"]
- "amount": number (optional, if mentioned)
- "category": string (optional, if mentioned)
- "note": string (optional)
- "date": string (optional, format: YYYY-MM-DD)
- "reply": a short confirmation message

Do not guess missing values. Use today's date if no date is provided and one is needed.

---

### Example Inputs and Outputs

**Input:**
spent 200 on lunch  
**Output:**
[
  {{
    "intent": "add_expense",
    "amount": 200,
    "category": "Lunch",
    "date": "{datetime.now().strftime('%Y-%m-%d')}",
    "reply": "₹200 expense added under Lunch."
  }}
]

**Input:**
earned 8000 from freelance  
**Output:**
[
  {{
    "intent": "add_income",
    "amount": 8000,
    "category": "Freelance",
    "date": "{datetime.now().strftime('%Y-%m-%d')}",
    "reply": "₹8,000 income added under Freelance."
  }}
]

**Input:**
how much money do I have left?  
**Output:**
[
  {{
    "intent": "get_summary",
    "reply": "Here is your current summary."
  }}
]

---

Now extract data from this message and return only the JSON array:

\"\"\"{user_message}\"\"\"
"""
# async def handle_chat(user_message: str, db, user_id: int) -> ChatResponseList:
#     prompt = build_prompt(user_message)
#     response = model.generate_content(prompt)
#     text = response.text.strip()

#     print("Gemini raw response:", text)
#     cleaned = re.sub(r"```json|```", "", text).strip()

#     try:
#         data = json.loads(cleaned)
#         if not isinstance(data, list):
#             data = [data]
#     except json.JSONDecodeError as e:
#         print("JSON decode error:", e)
#         return ChatResponseList(responses=[
#             ChatResponse(intent="error", note="Failed to parse model response as JSON.")
#         ])

#     print("Parsed JSON:", data)

#     expense_entries = []
#     income_entries = []
#     saving_entries = []
#     fallbacks = []

#     for entry in data:
#         # ✅ Ensure date exists
#         if not entry.get("date"):
#             entry["date"] = datetime.now().strftime("%Y-%m-%d")

#         intent = entry.get("intent", "unknown").lower().strip()

#         try:
#             parsed_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
#         except Exception:
#             parsed_date = datetime.now().date()

#         if intent == "add_expense" and "amount" in entry and "category" in entry:
#             expense_entries.append(ExpenseCreate(
#                 amount=entry["amount"],
#                 category=entry["category"],
#                 date=parsed_date,
#                 note=entry.get("note", "")
#             ))
#         elif intent == "add_income" and "amount" in entry and "category" in entry:
#             income_entries.append(IncomeCreate(
#                 amount=entry["amount"],
#                 category=entry["category"],
#                 date=parsed_date,
#                 note=entry.get("note", "")
#             ))
#         elif intent == "add_saving" and "amount" in entry and "category" in entry:
#             saving_entries.append(SavingCreate(
#                 amount=entry["amount"],
#                 category=entry["category"],
#                 date=parsed_date,
#                 note=entry.get("note", ""),
#                 title=entry.get("title", "Unnamed Saving")
#             ))
#         else:
#             # fallback: return the info to user if partial
#             fallbacks.append(ChatResponse(
#                 intent=intent,
#                 amount=entry.get("amount"),
#                 category=entry.get("category"),
#                 date=entry.get("date"),
#                 note=entry.get("note", ""),
#                 reply=entry.get("reply", "Got it.")
#             ))

#     responses = []

#     if expense_entries:
#         stored_expenses = await add_expenses_bulk(db, expense_entries, user_id=user_id)
#         for exp in stored_expenses:
#             responses.append(ChatResponse(
#                 intent="add_expense",
#                 amount=exp.amount,
#                 category=exp.category,
#                 date=exp.date.strftime("%Y-%m-%d"),
#                 note=exp.note,
#                 reply=next((e.get("reply") for e in data if e.get("amount") == exp.amount and e.get("category") == exp.category), "Added expense.")
#             ))

#     if income_entries:
#         stored_incomes = await add_incomes_bulk(db, income_entries, user_id=user_id)
#         for inc in stored_incomes:
#             responses.append(ChatResponse(
#                 intent="add_income",
#                 amount=inc.amount,
#                 category=inc.category,
#                 date=inc.date.strftime("%Y-%m-%d"),
#                 note=inc.note,
#                 reply=next((i.get("reply") for i in data if i.get("amount") == inc.amount and i.get("category") == inc.category), "Added income.")
#             ))

#     if saving_entries:
#         stored_savings = await add_savings_bulk(db, saving_entries, user_id=user_id)
#         for save in stored_savings:
#             responses.append(ChatResponse(
#                 intent="add_saving",
#                 amount=save.amount,
#                 category=save.category,
#                 date=save.date.strftime("%Y-%m-%d"),
#                 note=save.note,
#                 reply=next((s.get("reply") for s in data if s.get("amount") == save.amount and s.get("category") == save.category), "Added saving.")
#             ))

#     responses.extend(fallbacks)
#     return ChatResponseList(responses=responses)
async def handle_chat(user_message: str, db, user_id: int) -> ChatResponseList:
    prompt = build_prompt(user_message)
    response = model.generate_content(prompt)
    text = response.text.strip()

    print("Gemini raw response:", text)
    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        data = json.loads(cleaned)
        if not isinstance(data, list):
            data = [data]
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return ChatResponseList(responses=[
            ChatResponse(intent="error", note="Failed to parse model response as JSON.")
        ])

    print("Parsed JSON:", data)

    expense_entries = []
    income_entries = []
    saving_entries = []
    fallbacks = []
    responses = []

    for entry in data:
        if not entry.get("date"):
            entry["date"] = datetime.now().strftime("%Y-%m-%d")

        intent = entry.get("intent", "unknown").lower().strip()

        try:
            parsed_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
        except Exception:
            parsed_date = datetime.now().date()

        if intent == "add_expense" and "amount" in entry and "category" in entry:
            expense_entries.append(ExpenseCreate(
                amount=entry["amount"],
                category=entry["category"],
                date=parsed_date,
                note=entry.get("note", "")
            ))
        elif intent == "add_income" and "amount" in entry and "category" in entry:
            income_entries.append(IncomeCreate(
                amount=entry["amount"],
                category=entry["category"],
                date=parsed_date,
                note=entry.get("note", "")
            ))
        elif intent == "add_saving" and "amount" in entry and "category" in entry:
            saving_entries.append(SavingCreate(
                amount=entry["amount"],
                category=entry["category"],
                date=parsed_date,
                note=entry.get("note", ""),
                title=entry.get("title", "Unnamed Saving")
            ))
        elif intent == "get_summary":
            summary = await get_summary(db, user_id)
            responses.append(ChatResponse(
                intent="get_summary",
                reply=(
                    f"📊 Summary:\n"
                    f"Total Income: ₹{summary.total_income}\n"
                    f"Total Expense: ₹{summary.total_expense}\n"
                    f"Total Savings: ₹{summary.total_savings}\n"
                    f"Remaining Balance: ₹{summary.remaining_savings}"
                )
            ))
        else:
            fallbacks.append(ChatResponse(
                intent=intent,
                amount=entry.get("amount"),
                category=entry.get("category"),
                date=entry.get("date"),
                note=entry.get("note", ""),
                reply=entry.get("reply", "Got it.")
            ))

    if expense_entries:
        stored_expenses = await add_expenses_bulk(db, expense_entries, user_id=user_id)
        for exp in stored_expenses:
            responses.append(ChatResponse(
                intent="add_expense",
                amount=exp.amount,
                category=exp.category,
                date=exp.date.strftime("%Y-%m-%d"),
                note=exp.note,
                reply=next((e.get("reply") for e in data if e.get("amount") == exp.amount and e.get("category") == exp.category), "Added expense.")
            ))

    if income_entries:
        stored_incomes = await add_incomes_bulk(db, income_entries, user_id=user_id)
        for inc in stored_incomes:
            responses.append(ChatResponse(
                intent="add_income",
                amount=inc.amount,
                category=inc.category,
                date=inc.date.strftime("%Y-%m-%d"),
                note=inc.note,
                reply=next((i.get("reply") for i in data if i.get("amount") == inc.amount and i.get("category") == inc.category), "Added income.")
            ))

    if saving_entries:
        stored_savings = await add_savings_bulk(db, saving_entries, user_id=user_id)
        for save in stored_savings: 
            responses.append(ChatResponse(
                intent="add_saving",
                amount=save.amount,
                category=save.category,
                date=save.date.strftime("%Y-%m-%d"),
                note=save.note,
                reply=next((s.get("reply") for s in data if s.get("amount") == save.amount and s.get("category") == save.category), "Added saving.")
            ))

    responses.extend(fallbacks)
    return ChatResponseList(responses=responses)
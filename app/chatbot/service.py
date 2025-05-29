# app/api/chatbot/service.py

import json
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from app.expense.schema import ExpenseCreate
from app.expense.service import add_expense
from app.chatbot.schema import ChatResponse

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


# Step 1: Build the smart prompt
def build_prompt(user_message: str) -> str:
    return f"""
You are a smart and structured personal finance assistant in an app.

Your task is to understand the user's intent and extract the following fields in proper JSON format.

Always respond **only** with a JSON object — do NOT include any explanation, natural language, or triple backticks.

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

Example Output (format your response exactly like this):

{{
  "intent": "add_expense",
  "amount": 500,
  "category": "groceries",
  "date": "2025-05-29",
  "note": "milk and vegetables"
}}

If some values are not mentioned, omit them instead of guessing. Respond with only valid fields.
"""
# Step 2: Send to Gemini
async def handle_chat(user_message: str) -> ChatResponse:
    prompt = build_prompt(user_message)
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Clean JSON
    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return ChatResponse(
            intent="error",
            note="Failed to parse model response as JSON."
        )

    # Get current date if not provided
    if "date" not in data:
        data["date"] = datetime.now().strftime("%Y-%m-%d")

    # Create ChatResponse with safe field access
    return ChatResponse(
        intent=data.get("intent", "unknown"),
        amount=data.get("amount"),
        category=data.get("category"),
        date=data.get("date"),
        note=data.get("note")
    )
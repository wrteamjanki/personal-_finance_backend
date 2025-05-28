# import os
# import json
# import pandas as pd
# from datetime import datetime
# from dotenv import load_dotenv
# import google.generativeai as genai
# import gradio as gr

# # Load environment variables
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("GEMINI_API_KEY not found in .env file!")

# # Configure Gemini
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel("gemini-1.5-pro")

# # CSV File Paths
# EXPENSE_FILE = "expenses.csv"
# INCOME_FILE = "incomes.csv"

# # Load existing data or initialize
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

# # 💬 Chatbot Handler
# def handle_message(message, history):
#     global df_expense, df_income
#     msg = message.lower().strip()

#     # 🔹 1. Income-related queries
#     if any(kw in msg for kw in ["total income", "how much i earned", "what is my income", "show total income", "earned till now"]):
#         return f"💰 Total Income: ₹{df_income['amount'].sum()}"

#     # 🔹 2. Expense-related queries
#     if any(kw in msg for kw in ["total expense", "how much i spent", "spent till now", "show total expense", "what is my expense", "expense amount"]):
#         return f"💸 Total Expense: ₹{df_expense['amount'].sum()}"

#     # 🔹 3. Summary / Net Savings
#     if any(kw in msg for kw in ["summary", "overall report", "net savings", "finance summary", "show summary", "give me summary"]):
#         income = df_income["amount"].sum()
#         expense = df_expense["amount"].sum()
#         savings = income - expense
#         return f"📊 Summary:\n💰 Total Income: ₹{income}\n💸 Total Expense: ₹{expense}\n💾 Net Savings: ₹{savings}"

#     # 🔹 4. Most spent category
#     if "most" in msg and "spent" in msg:
#         if df_expense.empty:
#             return "ℹ️ No expense data found."
#         top_cat = df_expense.groupby("category")["amount"].sum().idxmax()
#         top_amt = df_expense.groupby("category")["amount"].sum().max()
#         return f"🧾 Most spent on '{top_cat}': ₹{top_amt}"

#     # 🔹 5. Add entries via Gemini
#     try:
#         entries = parse_entry(message)
#         if not entries:
#             return "🤔 I couldn't understand any valid entries."

#         responses = []
#         for entry in entries:
#             row = {
#                 "amount": entry.get("amount"),
#                 "category": entry.get("category", "Other"),
#                 "date": entry.get("date"),
#                 "note": entry.get("note", "")
#             }
#             if entry["type"] == "expense":
#                 df_expense = pd.concat([df_expense, pd.DataFrame([row])], ignore_index=True)
#                 responses.append(f"💸 Expense of ₹{row['amount']} on {row['category']} saved.")
#             elif entry["type"] == "income":
#                 df_income = pd.concat([df_income, pd.DataFrame([row])], ignore_index=True)
#                 responses.append(f"💰 Income of ₹{row['amount']} on {row['category']} saved.")

#         # Save to files
#         df_expense.to_csv(EXPENSE_FILE, index=False)
#         df_income.to_csv(INCOME_FILE, index=False)

#         return "\n".join(responses)

#     except Exception as e:
#         return str(e)


# # 🎨 Gradio Interface
# chat_interface = gr.ChatInterface(
#     fn=handle_message,
#     title="💸 FineTrack – Gemini Finance Assistant",
#     chatbot=gr.Chatbot(height=800, type="messages"),
#     textbox=gr.Textbox(placeholder="e.g. I earned 8000 and spent 2000 on rent and 500 on groceries", container=False),
#     theme="soft"
# )

# if __name__ == "__main__":
#     chat_interface.launch()
from fastapi import FastAPI
from app.core.config import settings
from app.expense.router import router as expense_router
from app.chatbot.router import router as chat_router
from app.income.router import router as income_router

app = FastAPI(
    title="Personal Finance Bot API",
    version="1.0"
)

# Include routers
app.include_router(expense_router)
app.include_router(chat_router, tags=["Chatbot"])
app.include_router(income_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Personal Finance Bot API"}

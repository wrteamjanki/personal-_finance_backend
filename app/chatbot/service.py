import csv
import json
import re
from datetime import datetime
from app.chatbot.prompt_template import build_prompt
from app.utils.gemini import call_gemini
from app.chatbot.schema import ChatResponse
import asyncio

def parse_gemini_response(response_text: str) -> ChatResponse:
    try:
        # Extract JSON object using regex
        json_match = re.search(r"\{.*?\}", response_text, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON object found in Gemini response.")

        json_str = json_match.group(0)
        json_data = json.loads(json_str)

        return ChatResponse(
            type=json_data["type"].lower(),
            amount=float(json_data["amount"]),
            category=json_data["category"],
            date=datetime.strptime(json_data["date"], "%Y-%m-%d").date(),
            note=json_data.get("note", ""),
            confirmation="Entry added successfully."
        )
    except Exception as e:
        print("❌ Gemini RAW response:\n", response_text)
        raise ValueError(f"❌ Failed to parse Gemini response: {e}")

def _write_to_csv(entry: ChatResponse):
    filename = "data/expenses.csv" if entry.type == "expense" else "data/income_saving.csv"
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([entry.date, entry.amount, entry.category, entry.note])

async def save_to_csv(entry: ChatResponse):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: _write_to_csv(entry))

async def handle_chat(message: str) -> ChatResponse:
    prompt = build_prompt(message)
    raw_response = await call_gemini(prompt)
    entry = parse_gemini_response(raw_response)
    await save_to_csv(entry)
    return entry

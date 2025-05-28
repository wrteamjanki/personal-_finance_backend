import google.generativeai as genai
from app.core.config import settings
import asyncio

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def call_gemini(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
    return response.text

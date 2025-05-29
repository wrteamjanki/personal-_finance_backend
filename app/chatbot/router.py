from fastapi import APIRouter
from app.chatbot.service import handle_chat
from app.chatbot.schema import ChatRequest, ChatResponse
from app.expense.service import add_expense
from app.income.service import add_income



router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    parsed_data = await handle_chat(request.message)
    intent = parsed_data.intent

    # Pass parsed data to respective modules
    if intent == "add_expense":
        await add_expense(parsed_data)
    elif intent == "add_income":
        await add_income(parsed_data)

    return parsed_data



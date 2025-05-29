from fastapi import APIRouter
from app.chatbot.service import handle_chat
<<<<<<< HEAD
from app.chatbot.schema import ChatRequest, ChatResponse
from app.expense.service import add_expense
from app.income.service import add_income


=======
from app.auth.dependencies import get_current_user
>>>>>>> 58f2f395c5250be0b665bc36d0f6748b7045e8b2

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
<<<<<<< HEAD
async def chat_endpoint(request: ChatRequest):
    parsed_data = await handle_chat(request.message)
    intent = parsed_data.intent

    # Pass parsed data to respective modules
    if intent == "add_expense":
        await add_expense(parsed_data)
    elif intent == "add_income":
        await add_income(parsed_data)

    return parsed_data


=======
async def chat(request: ChatRequest, token: str = Depends(get_current_user)):
    return await handle_chat(request.message)
>>>>>>> 58f2f395c5250be0b665bc36d0f6748b7045e8b2

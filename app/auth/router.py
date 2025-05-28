from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt_utils import create_access_token
from app.auth.service import authenticate_user

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

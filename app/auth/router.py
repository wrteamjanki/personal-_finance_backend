# app/auth/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import LoginRequest, TokenResponse
from app.auth.service import authenticate_user
from app.auth.jwt_utils import create_access_token
from app.db.database import get_async_session

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login_user(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(db, login_data.username, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token_data = {"sub": str(user.id)}
    access_token = create_access_token(token_data)

    return TokenResponse(access_token=access_token, token_type="bearer")

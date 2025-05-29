from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt_utils import create_access_token, verify_token
from app.auth.service import authenticate_user
from app.auth.schemas import Token, User
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify-token")
async def verify_token_endpoint(token: str):
    try:
        payload = verify_token(token)
        return {"valid": True, "username": payload.get("sub")}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=User)
async def read_users_me(user: dict = Depends(get_current_user)):
    return {
        "username": user["username"],
        "full_name": "Test User",
        "disabled": False
    }

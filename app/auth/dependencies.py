from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_async_session
from app.auth.jwt_utils import decode_access_token  # Use the same decoder you were using earlier
from app.db.models import User

async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise credentials_exception

        token = authorization.removeprefix("Bearer ").strip()
        payload = decode_access_token(token)

        if not payload or "sub" not in payload:
            raise credentials_exception

        user_id = payload["sub"]

        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception

        return user

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error in get_current_user:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal authentication error"
        )

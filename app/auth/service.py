# app/auth/service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from app.db.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

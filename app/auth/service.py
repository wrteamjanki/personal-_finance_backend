# Remove or comment out these lines:
# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)

# Add this import instead:
from app.auth.password_utils import verify_password, get_password_hash
from app.auth.schemas import UserInDB
from app.auth.fake_db import fake_users_db

async def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

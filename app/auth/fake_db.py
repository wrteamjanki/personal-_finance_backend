from app.auth.schemas import UserInDB
from app.auth.service import get_password_hash

fake_users_db = {
    "testuser": UserInDB(
        username="testuser",
        full_name="Test User",
        hashed_password=get_password_hash("testpass123"),
        disabled=False
    ),
    "admin": UserInDB(
        username="admin",
        full_name="Admin User",
        hashed_password=get_password_hash("admin123"),
        disabled=False
    )
}

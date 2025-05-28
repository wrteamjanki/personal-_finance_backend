from app.auth.utils import get_password_hash

fake_users_db = {
    "boss": {
        "username": "boss",
        "full_name": "The Boss",
        "hashed_password": get_password_hash("supersecretpassword"),
        "disabled": False,
    }
}

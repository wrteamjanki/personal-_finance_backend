# dummy user auth — replace with DB check
async def authenticate_user(username: str, password: str):
    if username == "admin" and password == "admin123":
        return {"username": username}
    return None

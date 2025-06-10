from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # ✅ Correct: type is `str`, default value is "bearer"

TokenResponse.model_rebuild()  # Optional unless you're getting "not fully defined" errors

from fastapi import FastAPI
from app.auth.router import router as auth_router
# import other routers ...

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# include other routers similarly

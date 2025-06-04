from fastapi import FastAPI
from app.auth.router import router as auth_router
# import other routers ...

app = FastAPI()

app.include_router(auth_router)  # mounts /auth routes

# include other routers similarly

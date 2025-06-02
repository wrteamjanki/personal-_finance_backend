from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# Async DB URL (e.g., postgresql+asyncpg://user:pass@localhost/db)
DATABASE_URL = settings.DATABASE_URL

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Base model
Base = declarative_base()

# Dependency for FastAPI
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

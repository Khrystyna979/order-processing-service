from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    ...

class DatabaseSessionManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        
    async def __aenter__(self):
        self.session = self.session_factory()
        return self.session
        
    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
            
            
async def get_db():
    async with DatabaseSessionManager(SessionLocal) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
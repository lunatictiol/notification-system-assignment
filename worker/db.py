from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import  Column, Integer, String, DateTime, func
from sqlalchemy.future import select

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@postgres:5432/fcm_db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class FCMToken(Base):
    __tablename__ = "device_tokens"
    id = Column(Integer, primary_key=True, index=True)
    fcm_token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

async def get_all_fcm_tokens(session: AsyncSession):
    result = await session.execute(select(FCMToken.fcm_token))
    tokens = result.scalars().all()
    return tokens
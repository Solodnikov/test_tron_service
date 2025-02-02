from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = "wallet_logs.db"
DATABASE_URL = f"sqlite+aiosqlite:///./{DATABASE_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine,
                            class_=AsyncSession,
                            expire_on_commit=False)
Base = declarative_base()

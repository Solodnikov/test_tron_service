import os
from contextlib import asynccontextmanager

from src.db import DATABASE_NAME, Base, SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from src.models import WalletLog
from src.schemas import WalletLogResponseList, WalletRequest, WalletResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from tronpy import Tron
from tronpy.providers import HTTPProvider


tron_client = Tron(HTTPProvider("https://api.shasta.trongrid.io"))


async def init_db():
    """Создает базу данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Проверяет создана ли база данных и создает, если нет."""
    if not os.path.exists(DATABASE_NAME):
        await init_db()
    yield

app = FastAPI(lifespan=lifespan)


async def get_db():
    """Создает сессию."""
    async with SessionLocal() as session:
        yield session


@app.post(
        "/getaccountresource",
        response_model=WalletResponse,
        description="Получение информации о кошельке",)
async def get_wallet_info(
        request: WalletRequest,
        db: AsyncSession = Depends(get_db),
):
    address = request.wallet_address
    try:
        bandwidth = tron_client.get_bandwidth(address)
        balance = tron_client.get_account_balance(address)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка при запросе: {str(e)}")
    # Сохраняем запрос в БД
    wallet_log = WalletLog(
        wallet_address=address,
        balance=balance,
        bandwidth=bandwidth
    )
    db.add(wallet_log)
    await db.commit()

    return WalletResponse(
        wallet_address=address,
        balance=balance,
        bandwidth=bandwidth
    )


@app.get("/wallet_logs", response_model=WalletLogResponseList)
async def get_wallet_logs(
        limit: int = 10,
        offset: int = 0,
        db: AsyncSession = Depends(get_db)
):
    query = await db.execute(select(WalletLog).offset(offset).limit(limit))
    logs = query.scalars().all()
    return {"logs": logs}


# TODO: how to get energy from adress
# method needs additional atributes
# get_estimated_energy(
#   owner_address: str,
#   contract_address: str,
#   function_selector: str,
#   parameter: str) → int

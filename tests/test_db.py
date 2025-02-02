import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db import Base, SessionLocal, engine
from src.main import app
from src.models import WalletLog


@pytest.fixture(scope="function")
async def test_db():
    # Создаем новую таблицу для каждого теста
    async with engine.begin() as conn:
        # Асинхронно удаляем все таблицы (если они существуют)
        await conn.run_sync(Base.metadata.drop_all)
        # Асинхронно создаем все таблицы заново
        await conn.run_sync(Base.metadata.create_all)

    # Создаем сессию для теста
    db = SessionLocal()
    yield db

    # После теста очищаем все данные
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db.close()

client = TestClient(app)


@pytest.mark.asyncio
async def test_getaccountresource(test_db: AsyncSession):
    """
    Тестирует ручку getaccountresource на получение корректной информации.
    Проверяет сохранение данных в базе данных.
    """
    wallet_address = "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"
    response = client.post(
        "/getaccountresource",
        json={"wallet_address": wallet_address}
    )
    assert response.status_code == 200
    data = response.json()
    assert 'wallet_address' in data
    assert 'balance' in data
    assert 'bandwidth' in data

    quary = select(WalletLog).filter(
        WalletLog.wallet_address == wallet_address)
    result = await test_db.execute(quary)
    wallet_log = result.scalars().first()

    assert wallet_log is not None
    assert wallet_log.wallet_address == wallet_address
    assert wallet_log.balance == data['balance']
    assert wallet_log.bandwidth == data['bandwidth']

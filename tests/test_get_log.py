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

    # Вставляем 4 моковых данных
    logs = [
        WalletLog(
            wallet_address="TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS21",
            balance=100.0,
            bandwidth=10),
        WalletLog(
            wallet_address="TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS22",
            balance=200.0,
            bandwidth=20),
        WalletLog(
            wallet_address="TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS23",
            balance=300.0,
            bandwidth=30),
        WalletLog(
            wallet_address="TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS24",
            balance=400.0,
            bandwidth=40),
    ]

    async with db.begin():
        db.add_all(logs)

    yield db

    # После теста очищаем все данные
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db.close()

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_wallet_logs(test_db: AsyncSession):
    """
    Тестирует ручку get_wallet_logs,
    проверяет корректность получения логов кошельков.
    """
    # Запрашиваем логи с лимитом 2 и сдвигом 0
    response = client.get("/wallet_logs?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()

    # Проверяем, что данные содержат список логов
    assert "logs" in data
    assert isinstance(data["logs"], list)
    assert len(data["logs"]) == 2  # Ожидаем 2 записи

    # Проверяем, что данные соответствуют записям в базе
    wallet_addresses = [log["wallet_address"] for log in data["logs"]]
    query = select(WalletLog).filter(
        WalletLog.wallet_address.in_(wallet_addresses))
    result = await test_db.execute(query)
    wallet_logs = result.scalars().all()

    assert len(wallet_logs) == 2  # Ожидаем 2 записи в базе

    # Сортируем оба списка по wallet_address для корректного сопоставления
    wallet_logs_sorted = sorted(
        wallet_logs, key=lambda log: log.wallet_address)
    data_logs_sorted = sorted(
        data["logs"], key=lambda log: log["wallet_address"])

    # Проверяем, что каждая запись в базе данных соответствует данным
    for log, log_data in zip(wallet_logs_sorted, data_logs_sorted):
        assert log.wallet_address == log_data["wallet_address"]
        assert log.balance == log_data["balance"]
        assert log.bandwidth == log_data["bandwidth"]

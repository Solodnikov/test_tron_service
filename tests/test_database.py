import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db import Base
from src.models import WalletLog


# Создаем тестовую базу данных (SQLite в памяти)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """Создает тестовую базу данных."""
    # Создаем таблицы перед каждым тестом
    Base.metadata.create_all(bind=engine)

    # Создаем сессию
    db = SessionLocal()
    yield db

    # Закрываем сессию и удаляем таблицы после теста
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_wallet_log(test_db):
    """Тестирует запись в базу данных."""

    # Проверяем, что в базе данных нет записей
    initial_count = test_db.query(WalletLog).count()
    assert initial_count == 0

    wallet_log = WalletLog(
        wallet_address="TCp3y2k3m1F4d6PjXv7z9Qp5Lk6N8M2B1D",
        balance=100.0,
        bandwidth=5000
    )

    # Добавляем запись в базу
    test_db.add(wallet_log)
    test_db.commit()
    test_db.refresh(wallet_log)

    # Проверяем, что теперь в базе данных есть ровно одна запись
    final_count = test_db.query(WalletLog).count()
    assert final_count == 1

    # Проверяем, что запись добавлена и содержит корректные данные
    result = test_db.query(WalletLog).filter_by(
        wallet_address=wallet_log.wallet_address).first()

    assert result is not None
    assert result.wallet_address == wallet_log.wallet_address
    assert result.balance == wallet_log.balance
    assert result.bandwidth == wallet_log.bandwidth

from db import Base
from sqlalchemy import Column, DateTime, Float, Integer, String, func


class WalletLog(Base):
    __tablename__ = "wallet_logs"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, index=True)
    balance = Column(Float)
    bandwidth = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now(), index=True)

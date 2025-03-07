from datetime import datetime
from typing import List

from pydantic import BaseModel


class WalletRequest(BaseModel):
    wallet_address: str = "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"


class WalletResponse(BaseModel):
    wallet_address: str
    balance: float
    bandwidth: int


class WalletLogResponse(BaseModel):
    wallet_address: str
    balance: float
    bandwidth: int
    timestamp: datetime


class WalletLogResponseList(BaseModel):
    logs: List[WalletLogResponse]

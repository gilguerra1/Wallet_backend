from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class WalletBalance(BaseModel):

    wallet_address: str = Field(..., max_length=64)
    currency_id: int = Field(...)
    balance: Decimal = Field(default=Decimal('0.0'), decimal_places=8)
    update_date: datetime = Field(...)

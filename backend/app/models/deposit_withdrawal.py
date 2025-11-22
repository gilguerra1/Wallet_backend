from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field


class DepositWithdrawal(BaseModel):

    movement_id: int = Field(...)
    wallet_address: str = Field(..., max_length=64)
    currency_id: int = Field(...)
    transaction_type: Literal["DEPOSITO", "SAQUE"] = Field(...)
    value: float = Field(...)
    fee_value: float = Field(default=0.0)
    transaction_date: datetime = Field(...)

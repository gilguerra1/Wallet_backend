from pydantic import BaseModel, Field
from typing import Optional


class Transfer(BaseModel):

    transfer_id: Optional[int] = Field(None)
    wallet_origin_address: str = Field(..., max_length=64)
    wallet_target_address: str = Field(..., max_length=64)
    currency_id: int = Field(...)
    value: float = Field(..., gt=0)
    fee_percentage: float = Field(..., ge=0, le=1)
    fee_value: float = Field(..., gt=0)
    transaction_date: str = Field(...)

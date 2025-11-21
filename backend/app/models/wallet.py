from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field


class Wallet(BaseModel):

    wallet_address: str = Field(..., max_length=64)
    private_key_hash: str = Field(..., max_length=64)
    creation_date: datetime = Field(...)
    status: Literal["ATIVA", "BLOQUEADA"] = Field(..., max_length=15)

class WalletCreate(BaseModel):
    
    wallet_address: str = Field(..., max_length=64)
    creation_date: datetime = Field(...)
    status: Literal["ATIVA", "BLOQUEADA"] = Field(..., max_length=15)
    private_key: str = Field(...)

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional


class Currency(BaseModel):
    
    currency_id: Optional[int] = Field(None, description="Auto-incremented primary key (SERIAL)")
    code: str = Field(..., max_length=10)
    name: str = Field(..., max_length=50)
    type_currency: str = Field(..., max_length=20)
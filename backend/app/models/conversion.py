from pydantic import BaseModel, Field
from typing import Optional


class Conversion(BaseModel):

    conversion_id: Optional[int] = Field(
        None, description="Auto-incremented primary key (SERIAL)")
    wallet_address: str = Field(..., max_length=64)
    source_currency_id: int = Field(
        ..., description="ID da moeda de origem"
    )
    target_currency_id: int = Field(
        ..., description="ID da moeda de destino"
    )
    source_value: float = Field(
        ..., gt=0, description="Valor da moeda de origem"
    )
    target_value: float = Field(
        ..., gt=0, description="Valor da moeda de destino"
    )
    fee_percentage: float = Field(
        ..., ge=0, le=1, description="Porcentagem da taxa aplicada"
    )
    fee_value: float = Field(..., gt=0, description="Valor da taxa aplicada")
    used_quotation: float = Field(..., gt=0, description="Cotação utilizada")
    transaction_date: str = Field(..., description="Data da transação")

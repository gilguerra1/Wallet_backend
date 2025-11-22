from datetime import datetime
from typing import Dict, Any
from sqlalchemy import text
from database.connection import get_connection
from app.core.config import WITHDRAWAL_FEE_RATE


class DepositWithdrawalRepository:

    def create_deposit_withdrawal(
        self,
        wallet_address: str,
        currency_id: int,
        transaction_type: str,
        value: float
    ) -> Dict[str, Any]:
        """
        Creates a deposit or withdrawal record in the database.
        Fee is applied based on transaction type:
        - DEPOSITO: fee_value = 0.0
        - SAQUE: fee_value = value * WITHDRAWAL_FEE_RATE
        """
        transaction_date = datetime.utcnow()

        # Determina o fee_value baseado no tipo de transação
        if transaction_type.upper() == "SAQUE":
            fee_value = value * WITHDRAWAL_FEE_RATE
        else:  # DEPOSITO
            fee_value = 0.0

        with get_connection() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO deposit_withdrawal (
                        wallet_address,
                        currency_id,
                        transaction_type,
                        value,
                        fee_value,
                        transaction_date
                    ) VALUES (
                        :wallet_address,
                        :currency_id,
                        :transaction_type,
                        :value,
                        :fee_value,
                        :transaction_date
                    )
                    RETURNING movement_id
                """),
                {
                    "wallet_address": wallet_address,
                    "currency_id": currency_id,
                    "transaction_type": transaction_type,
                    "value": value,
                    "fee_value": fee_value,
                    "transaction_date": transaction_date
                }
            )
            movement_id = result.scalar_one()
            return {
                "movement_id": movement_id,
                "wallet_address": wallet_address,
                "currency_id": currency_id,
                "transaction_type": transaction_type,
                "value": value,
                "fee_value": fee_value,
                "transaction_date": transaction_date
            }

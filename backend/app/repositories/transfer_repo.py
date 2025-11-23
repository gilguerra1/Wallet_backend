from datetime import datetime
from sqlalchemy import text
from database.connection import get_connection


class TransferRepository:

    def create_transfer(
        self,
        wallet_origin_address: str,
        wallet_target_address: str,
        currency_id: int,
        value: float,
        fee_value: float
    ):
        """
        Creates a transfer record in the database.
        """
        transaction_date = datetime.now()

        with get_connection() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO transfer (
                        wallet_origin_address,
                        wallet_target_address,
                        currency_id,
                        value,
                        fee_value,
                        transaction_date
                    ) VALUES (
                        :wallet_origin_address,
                        :wallet_target_address,
                        :currency_id,
                        :value,
                        :fee_value,
                        :transaction_date
                    )
                    RETURNING transfer_id
                """),
                {
                    "wallet_origin_address": wallet_origin_address,
                    "wallet_target_address": wallet_target_address,
                    "currency_id": currency_id,
                    "value": value,
                    "fee_value": fee_value,
                    "transaction_date": transaction_date
                }
            )
            transfer_id = result.scalar_one()
            return {
                "transfer_id": transfer_id,
                "wallet_origin_address": wallet_origin_address,
                "wallet_target_address": wallet_target_address,
                "currency_id": currency_id,
                "value": value,
                "fee_value": fee_value,
                "transaction_date": transaction_date
            }

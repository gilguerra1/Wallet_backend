from sqlalchemy import text
from database.connection import get_connection


class ConversionRepository:

    def createConversion(self, conversion_data):
        with get_connection() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO conversion (
                        wallet_address,
                        source_currency_id,
                        target_currency_id,
                        source_value,
                        target_value,
                        fee_percentage,
                        fee_value,
                        used_quotation,
                        transaction_date
                    ) VALUES (
                        :wallet_address,
                        :source_currency_id,
                        :target_currency_id,
                        :source_value,
                        :target_value,
                        :fee_percentage,
                        :fee_value,
                        :used_quotation,
                        :transaction_date
                    )
                    RETURNING conversion_id
                """),
                conversion_data
            )
            conversion_id = result.scalar_one_or_none()

        return conversion_id

from sqlalchemy import text
from database.connection import get_connection


class CurrencyRepository:

    def getCurrencyById(self, currency_id):
        with get_connection() as conn:
            row = conn.execute(
                text("""
                    SELECT currency_id, code, name, type_currency
                    FROM currency
                    WHERE currency_id = :currency_id
                """),
                {"currency_id": currency_id}
            ).mappings().first()

        if row:
            return dict(row)
        return None

    def getAllCurrencies(self):
        with get_connection() as conn:
            rows = conn.execute(
                text("""
                    SELECT currency_id, code, name, type_currency
                    FROM currency
                    ORDER BY currency_id
                """)
            ).mappings().fetchall()

        return [dict(row) for row in rows]

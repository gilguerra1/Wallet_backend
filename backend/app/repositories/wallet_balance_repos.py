# coding: utf-8
from typing import List, Dict, Any
from sqlalchemy import text
from database.connection import get_connection


class WalletBalanceRepository:

    def get_balances_by_wallet_address(
            self, wallet_address: str) -> List[Dict[str, Any]]:
        """
        Retrieves all currency balances for a specific wallet.
        Returns all currencies with balance 0.0 if no balance exists.
        """
        with get_connection() as conn:
            rows = conn.execute(
                text("""
                    SELECT
                        c.currency_id,
                        c.code as currency_code,
                        c.name as currency_name,
                        c.type_currency,
                        COALESCE(wb.balance, 0.0) as balance,
                        COALESCE(
                            wb.update_date, CURRENT_TIMESTAMP
                        ) as update_date
                    FROM currency c
                    LEFT JOIN wallet_balance wb
                        ON c.currency_id = wb.currency_id
                        AND wb.wallet_address = :wallet_address
                    ORDER BY c.currency_id
                """),
                {"wallet_address": wallet_address}
            ).mappings().fetchall()

        return [dict(row) for row in rows]

    def create_initial_balances(
            self, wallet_address: str
    ) -> None:
        """
        Creates initial balance records for all currencies
        when a wallet is created.
        """
        with get_connection() as conn:
            conn.execute(
                text("""
                    INSERT INTO wallet_balance (
                        wallet_address, currency_id, balance,
                        update_date
                    )
                    SELECT :wallet_address, currency_id, 0.0,
                           CURRENT_TIMESTAMP
                    FROM currency
                    ON CONFLICT (wallet_address, currency_id)
                    DO NOTHING
                """),
                {"wallet_address": wallet_address}
            )

    def update_balance(
            self,
            wallet_address: str,
            currency_id: int,
            amount: float) -> None:
        """
        Updates the balance of a wallet for a specific currency.
        Positive amount for deposits, negative for withdrawals.
        Creates the balance record if it doesn't exist.
        """
        with get_connection() as conn:
            conn.execute(
                text("""
                    INSERT INTO wallet_balance (
                        wallet_address, currency_id, balance,
                        update_date
                    )
                    VALUES (
                        :wallet_address, :currency_id, :amount,
                        CURRENT_TIMESTAMP
                    )
                    ON CONFLICT (wallet_address, currency_id)
                    DO UPDATE SET
                        balance = wallet_balance.balance + :amount,
                        update_date = CURRENT_TIMESTAMP
                """),
                {
                    "wallet_address": wallet_address,
                    "currency_id": currency_id,
                    "amount": amount
                }
            )

    def get_balance(self, wallet_address: str, currency_id: int) -> float:
        """
        Gets the current balance for a specific wallet and currency.
        Returns 0.0 if balance record doesn't exist.
        """
        with get_connection() as conn:
            result = conn.execute(
                text("""
                    SELECT COALESCE(balance, 0.0) as balance
                    FROM wallet_balance
                    WHERE wallet_address = :wallet_address
                      AND currency_id = :currency_id
                """),
                {
                    "wallet_address": wallet_address,
                    "currency_id": currency_id
                }
            ).mappings().fetchone()

            return float(result["balance"]) if result else 0.0

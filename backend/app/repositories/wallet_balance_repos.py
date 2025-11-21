# coding: utf-8
from typing import List, Dict, Any
from sqlalchemy import text
from database.connection import get_connection

class WalletBalanceRepository:
    
    def get_balances_by_wallet_address(self, wallet_address: str) -> List[Dict[str, Any]]:
        """
        Retrieves all currency balances for a specific wallet.
        Returns all currencies with balance 0.0 if no balance exists.
        """
        with get_connection() as conn:
            # Query que faz LEFT JOIN para mostrar todas as moedas, mesmo com saldo 0
            rows = conn.execute(
                text("""
                    SELECT 
                        c.currency_id,
                        c.code as currency_code,
                        c.name as currency_name,
                        c.type_currency,
                        COALESCE(wb.balance, 0.0) as balance,
                        COALESCE(wb.update_date, CURRENT_TIMESTAMP) as update_date
                    FROM currency c
                    LEFT JOIN wallet_balance wb ON c.currency_id = wb.currency_id 
                                                AND wb.wallet_address = :wallet_address
                    ORDER BY c.currency_id
                """),
                {"wallet_address": wallet_address}
            ).mappings().fetchall()
            
        return [dict(row) for row in rows]
    
    def create_initial_balances(self, wallet_address: str) -> None:
        """
        Creates initial balance records for all currencies when a wallet is created.
        """
        with get_connection() as conn:
            # Insere saldo 0 para todas as moedas disponíveis
            conn.execute(
                text("""
                    INSERT INTO wallet_balance (wallet_address, currency_id, balance, update_date)
                    SELECT :wallet_address, currency_id, 0.0, CURRENT_TIMESTAMP
                    FROM currency
                    ON CONFLICT (wallet_address, currency_id) DO NOTHING
                """),
                {"wallet_address": wallet_address}
            )

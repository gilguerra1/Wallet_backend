# coding: utf-8
from typing import List
from app.repositories.wallet_balance_repos import WalletBalanceRepository


class WalletBalanceService:

    def __init__(
            self,
            wallet_balance_repo: WalletBalanceRepository = None
    ):
        self.wallet_balance_repo = (
            wallet_balance_repo or WalletBalanceRepository()
        )

    def get_wallet_balances(self, wallet_address: str) -> List[dict]:
        """
        Retrieves all currency balances for a wallet address.
        Returns balances with currency information.
        """
        balances = self.wallet_balance_repo.get_balances_by_wallet_address(
            wallet_address)

        # Format response
        result = []
        for balance in balances:
            result.append({
                "currency_id": balance["currency_id"],
                "currency_code": balance["currency_code"],
                "currency_name": balance["currency_name"],
                "type_currency": balance["type_currency"],
                # Convert Decimal to string
                "balance": str(balance["balance"]),
                "update_date": balance["update_date"]
            })

        return result

    def initialize_wallet_balances(self, wallet_address: str) -> None:
        """
        Creates initial balance records for all currencies.
        """
        self.wallet_balance_repo.create_initial_balances(wallet_address)

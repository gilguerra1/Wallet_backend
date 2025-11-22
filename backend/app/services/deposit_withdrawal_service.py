from typing import Literal

from app.repositories.deposit_withdrawal_repo import (
    DepositWithdrawalRepository
)
from app.repositories.wallet_balance_repos import WalletBalanceRepository
from app.models.deposit_withdrawal import DepositWithdrawal
from app.core.config import WITHDRAWAL_FEE_RATE


class DepositWithdrawalService:

    def __init__(
            self,
            deposit_withdrawal_repo: DepositWithdrawalRepository = None,
            wallet_balance_repo: WalletBalanceRepository = None):
        self.deposit_withdrawal_repo = (
            deposit_withdrawal_repo or
            DepositWithdrawalRepository()
        )
        self.wallet_balance_repo = (
            wallet_balance_repo or
            WalletBalanceRepository()
        )

    def create_deposit_withdrawal(
        self,
        wallet_address: str,
        currency_id: int,
        transaction_type: Literal["DEPOSITO", "SAQUE"],
        value: float
    ) -> DepositWithdrawal:
        """
        Creates a deposit or withdrawal by calling the repository.
        Applies fee based on transaction type and updates wallet balance.
        Validates sufficient balance for withdrawals.
        """

        # Validação de saldo para saques
        if transaction_type.upper() == "SAQUE":
            current_balance = self.wallet_balance_repo.get_balance(
                wallet_address, currency_id)
            fee_value = value * WITHDRAWAL_FEE_RATE
            total_required = value + fee_value

            if current_balance < total_required:
                raise ValueError(
                    f"Saldo insuficiente. Saldo atual: {current_balance:.2f}, "
                    f"Valor do saque: {value:.2f}, Taxa: {fee_value:.2f}, "
                    f"Total necessário: {total_required:.2f}"
                )

        row = self.deposit_withdrawal_repo.create_deposit_withdrawal(
            wallet_address=wallet_address,
            currency_id=currency_id,
            transaction_type=transaction_type,
            value=value
        )

        # Atualiza o saldo da carteira
        if transaction_type.upper() == "DEPOSITO":
            # Depósito: adiciona o valor ao saldo
            self.wallet_balance_repo.update_balance(
                wallet_address, currency_id, value)
        else:  # SAQUE
            # Saque: subtrai o valor + taxa do saldo
            total_deducted = value + row["fee_value"]
            self.wallet_balance_repo.update_balance(
                wallet_address, currency_id, -total_deducted)

        return DepositWithdrawal(
            movement_id=row["movement_id"],
            wallet_address=wallet_address,
            currency_id=currency_id,
            transaction_type=transaction_type,
            value=value,
            fee_value=row["fee_value"],
            transaction_date=row["transaction_date"]
        )

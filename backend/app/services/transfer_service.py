from decimal import Decimal
from app.repositories.transfer_repo import TransferRepository
from app.repositories.wallet_balance_repos import WalletBalanceRepository
from app.core.config import TRANSFER_FEE_RATE


class TransferService:

    def __init__(
            self,
            transfer_repo: TransferRepository = None,
            wallet_balance_repo: WalletBalanceRepository = None
    ):
        self.transfer_repo = transfer_repo or TransferRepository()
        self.wallet_balance_repo = (
            wallet_balance_repo or WalletBalanceRepository()
        )

    def create_transfer(
            self,
            wallet_origin_address: str,
            wallet_target_address: str,
            currency_id: int,
            value: float
    ):

        # Calcula a taxa
        fee_value = Decimal(str(value)) * Decimal(str(TRANSFER_FEE_RATE))
        total_debit = Decimal(str(value)) + fee_value

        # Verifica saldo
        balance = self.wallet_balance_repo.get_balance(
            wallet_origin_address, currency_id
        )
        if balance < total_debit:
            raise ValueError("Saldo insuficiente")

        # Salva transferencia
        transfer_data = self.transfer_repo.create_transfer(
            wallet_origin_address,
            wallet_target_address,
            currency_id,
            float(value),
            float(fee_value)
        )

        # Debita origem (valor + taxa)
        self.wallet_balance_repo.update_balance(
            wallet_origin_address,
            currency_id,
            -float(total_debit)
        )

        # Credita destino (apenas valor)
        self.wallet_balance_repo.update_balance(
            wallet_target_address,
            currency_id,
            float(value)
        )

        return transfer_data

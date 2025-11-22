# coding: utf-8
from app.repositories.wallet_repo import WalletRepository
from app.models.wallet import WalletCreate, Wallet


class WalletService:

    def __init__(self, wallet_repo: WalletRepository = None):
        self.wallet_repo = wallet_repo or WalletRepository()

    def create_wallet(self) -> WalletCreate:
        """
        Creates a new wallet by calling the repository.
        Returns wallet data including private key in plain text.
        """

        row = self.wallet_repo.createWallet()
        return WalletCreate(
            wallet_address=row["wallet_address"],
            creation_date=row["creation_date"],
            status=row["status"],
            private_key=row["private_key"]
        )

    def get_wallet_by_address(self, wallet_address: str) -> Wallet:
        """
        Retrieves a wallet by its address.
        """

        row = self.wallet_repo.get_wallet_by_address(wallet_address)
        if not row:
            raise ValueError("Wallet not found")

        return Wallet(
            wallet_address=row["wallet_address"],
            private_key_hash=row["private_key_hash"],
            creation_date=row["creation_date"],
            status=row["status"]
        )

    def validate_private_key(
            self,
            wallet_address: str,
            private_key: str) -> bool:
        """
        Validates if the provided private key matches the wallet's stored hash.
        """
        return self.wallet_repo.validate_private_key(
            wallet_address, private_key)

import requests
from datetime import datetime
from app.repositories.conversion_repo import ConversionRepository
from app.repositories.wallet_balance_repos import WalletBalanceRepository
from app.repositories.currency_repos import CurrencyRepository
from app.models.conversion import Conversion
from app.core.config import CONVERSION_FEE_RATE, COINBASE_API_BASE_URL


class ConversionService:

    def __init__(self):
        self.conversion_repo = ConversionRepository()
        self.wallet_balance_repo = WalletBalanceRepository()
        self.currency_repo = CurrencyRepository()

    def get_coinbase_spot_price(self, from_currency, to_currency):
        url = (
            f"{COINBASE_API_BASE_URL}/"
            f"{from_currency}-{to_currency}/spot"
        )

        response = requests.get(url)
        data = response.json()
        price = float(data["data"]["amount"])

        return price

    def create_conversion(
            self, wallet_address, source_currency_id,
            target_currency_id, source_value):
        source_currency = self.currency_repo.getCurrencyById(
            source_currency_id
        )
        target_currency = self.currency_repo.getCurrencyById(
            target_currency_id
        )

        if not source_currency or not target_currency:
            raise ValueError("Moeda não encontrada")

        source_code = source_currency["code"]
        target_code = target_currency["code"]

        current_balance = self.wallet_balance_repo.get_balance(
            wallet_address, source_currency_id
        )

        if current_balance < source_value:
            raise ValueError("Saldo insuficiente")

        exchange_rate = self.get_coinbase_spot_price(
            source_code, target_code
        )

        converted_value = source_value * exchange_rate
        fee_value = converted_value * CONVERSION_FEE_RATE
        target_value = converted_value - fee_value

        conversion_data = {
            "wallet_address": wallet_address,
            "source_currency_id": source_currency_id,
            "target_currency_id": target_currency_id,
            "source_value": source_value,
            "target_value": target_value,
            "fee_percentage": CONVERSION_FEE_RATE,
            "fee_value": fee_value,
            "used_quotation": exchange_rate,
            "transaction_date": datetime.utcnow()
        }

        conversion_id = self.conversion_repo.createConversion(
            conversion_data
        )

        self.wallet_balance_repo.update_balance(
            wallet_address, source_currency_id, -source_value)
        self.wallet_balance_repo.update_balance(
            wallet_address, target_currency_id, target_value)

        return Conversion(
            conversion_id=conversion_id,
            wallet_address=wallet_address,
            source_currency_id=source_currency_id,
            target_currency_id=target_currency_id,
            source_value=source_value,
            target_value=target_value,
            fee_percentage=CONVERSION_FEE_RATE,
            fee_value=fee_value,
            used_quotation=exchange_rate,
            transaction_date=conversion_data["transaction_date"].isoformat()
        )

import os
from dotenv import load_dotenv


load_dotenv()

WITHDRAWAL_FEE_RATE = float(os.getenv("TAXA_SAQUE_PERCENTUAL"))
CONVERSION_FEE_RATE = float(os.getenv("TAXA_CONVERSAO_PERCENTUAL"))
TRANSFER_FEE_RATE = float(os.getenv("TAXA_TRANSFERENCIA_PERCENTUAL"))

COINBASE_API_BASE_URL = os.getenv("COINBASE_API_BASE_URL")

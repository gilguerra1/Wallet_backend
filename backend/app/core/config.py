import os
from dotenv import load_dotenv


load_dotenv()

# Business Rules
WITHDRAWAL_FEE_RATE = float(os.getenv("TAXA_SAQUE_PERCENTUAL", "0.01"))

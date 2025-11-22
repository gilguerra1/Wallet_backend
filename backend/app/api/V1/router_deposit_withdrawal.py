from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.services.deposit_withdrawal_service import (
    DepositWithdrawalService
)
from app.services.wallet_service import WalletService
from app.models.deposit_withdrawal import DepositWithdrawal
from app.repositories.deposit_withdrawal_repo import (
    DepositWithdrawalRepository
)
from app.repositories.wallet_repo import WalletRepository


router = APIRouter(prefix="/wallets", tags=["deposits-withdrawals"])


class DepositRequest(BaseModel):
    currency_id: int = Field(..., description="ID da moeda")
    value: float = Field(..., gt=0, description="Valor do depósito")
    private_key: str = Field(
        ..., min_length=1, description="Chave privada da carteira"
    )


class WithdrawalRequest(BaseModel):
    currency_id: int = Field(..., description="ID da moeda")
    value: float = Field(..., gt=0, description="Valor do saque")
    private_key: str = Field(
        ..., min_length=1, description="Chave privada da carteira"
    )


# Dependencies
def get_deposit_withdrawal_service() -> DepositWithdrawalService:
    repo = DepositWithdrawalRepository()
    return DepositWithdrawalService(repo)


def get_wallet_service() -> WalletService:
    repo = WalletRepository()
    return WalletService(repo)


@router.post(
    "/{address}/deposits", response_model=DepositWithdrawal,
    status_code=201
)
def create_deposit(
    address: str,
    request: DepositRequest,
    wallet_service: WalletService = Depends(get_wallet_service),
    deposit_service: DepositWithdrawalService = Depends(
        get_deposit_withdrawal_service
    ),
) -> DepositWithdrawal:
    """
    Cria um depósito para a carteira especificada.
    - Taxa de depósito: 0% (sem taxa)
    - Requer validação da chave privada
    """
    try:
        # Valida a chave privada
        is_valid = wallet_service.validate_private_key(
            address, request.private_key
        )
        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Chave privada inválida"
            )

        # Cria o depósito
        deposit = deposit_service.create_deposit_withdrawal(
            wallet_address=address,
            currency_id=request.currency_id,
            transaction_type="DEPOSITO",
            value=request.value
        )

        return deposit

    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{address}/withdrawals",
             response_model=DepositWithdrawal,
             status_code=201)
def create_withdrawal(
    address: str,
    request: WithdrawalRequest,
    wallet_service: WalletService = Depends(get_wallet_service),
    deposit_service: DepositWithdrawalService = Depends(
        get_deposit_withdrawal_service
    ),
) -> DepositWithdrawal:
    """
    Cria um saque para a carteira especificada.
    - Taxa de saque: 1% (configurável via TAXA_SAQUE_PERCENTUAL no .env)
    - Requer validação da chave privada
    """
    try:
        # Valida a chave privada
        is_valid = wallet_service.validate_private_key(
            address, request.private_key
        )
        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Chave privada inválida"
            )

        # Cria o saque
        withdrawal = deposit_service.create_deposit_withdrawal(
            wallet_address=address,
            currency_id=request.currency_id,
            transaction_type="SAQUE",
            value=request.value
        )

        return withdrawal

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.services.transfer_service import TransferService
from app.services.wallet_service import WalletService
from app.repositories.wallet_repo import WalletRepository


router = APIRouter(prefix="/wallets", tags=["transfer"])


class TransferRequest(BaseModel):
    wallet_target_address: str = Field(...)
    currency_id: int = Field(...)
    value: float = Field(..., gt=0)
    private_key: str = Field(..., min_length=1)


def get_transfer_service() -> TransferService:
    return TransferService()


def get_wallet_service() -> WalletService:
    repo = WalletRepository()
    return WalletService(repo)


@router.post("/{endereco_origem}/transfer", status_code=201)
def create_transfer(
    endereco_origem: str,
    request: TransferRequest,
    wallet_service: WalletService = Depends(get_wallet_service),
    transfer_service: TransferService = Depends(get_transfer_service),
):

    # Valida chave privada
    is_valid = wallet_service.validate_private_key(
        endereco_origem, request.private_key
    )
    if not is_valid:
        raise HTTPException(status_code=401, detail="Chave privada inválida")

    # Verifica se carteiras são diferentes
    if endereco_origem == request.wallet_target_address:
        raise HTTPException(
            status_code=400,
            detail="Não é possível transferir para a mesma carteira"
        )

    # Faz a transferencia
    transfer = transfer_service.create_transfer(
        wallet_origin_address=endereco_origem,
        wallet_target_address=request.wallet_target_address,
        currency_id=request.currency_id,
        value=request.value
    )

    return transfer

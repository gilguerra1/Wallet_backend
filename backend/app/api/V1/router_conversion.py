from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.conversion_service import ConversionService
from app.services.wallet_service import WalletService
from app.models.conversion import Conversion


router = APIRouter(prefix="/wallets", tags=["Conversions"])


class ConversionRequest(BaseModel):
    source_currency_id: int
    target_currency_id: int
    source_value: float
    private_key: str


def get_conversion_service():
    return ConversionService()


def get_wallet_service():
    return WalletService()


@router.post("/{address}/conversions", response_model=Conversion,
             status_code=201)
def create_conversion(
        address: str,
        request: ConversionRequest,
        wallet_service: WalletService = Depends(get_wallet_service),
        conversion_service: ConversionService = Depends(
            get_conversion_service)):
    try:
        # Valida chave privada
        is_valid = wallet_service.validate_private_key(
            address, request.private_key
        )
        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Chave privada inválida"
            )

        # Verifica se as moedas são diferentes
        if request.source_currency_id == request.target_currency_id:
            raise HTTPException(
                status_code=400,
                detail="As moedas devem ser diferentes"
            )

        # Faz a conversão
        conversion = conversion_service.create_conversion(
            address,
            request.source_currency_id,
            request.target_currency_id,
            request.source_value
        )

        return conversion

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

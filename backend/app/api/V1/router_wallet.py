# coding: utf-8
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.services.wallet_service import WalletService
from app.services.wallet_balance_service import WalletBalanceService
from app.models.wallet import WalletCreate, Wallet
from app.repositories.wallet_repo import WalletRepository
from app.repositories.wallet_balance_repos import WalletBalanceRepository


router = APIRouter(prefix="/wallets", tags=["wallets"])

def get_wallet_service() -> WalletService:
    repo = WalletRepository()
    return WalletService(repo)

def get_wallet_balance_service() -> WalletBalanceService:
    repo = WalletBalanceRepository()
    return WalletBalanceService(repo)

@router.post("", response_model=WalletCreate, status_code=201)
def create_wallet(
    wallet_service: WalletService = Depends(get_wallet_service),
) -> WalletCreate:
    """
    Cria uma nova carteira.
    """
    try:
        wallet = wallet_service.create_wallet()
        return wallet
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{wallet_address}", response_model=Wallet)
def get_wallet(
    wallet_address: str,
    wallet_service: WalletService = Depends(get_wallet_service),
) -> Wallet:
    """
    Recupera uma carteira pelo seu endereço.
    """
    try:
        wallet = wallet_service.get_wallet_by_address(wallet_address)
        return wallet
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))

@router.get("/{wallet_address}/balance")
def get_wallet_balances(
    wallet_address: str,
    wallet_service: WalletService = Depends(get_wallet_service),
    balance_service: WalletBalanceService = Depends(get_wallet_balance_service),
):
    """
    Recupera todos os saldos de uma carteira por endereço.
    Retorna saldos de todas as moedas disponíveis.
    """
    try:
        wallet_service.get_wallet_by_address(wallet_address)
        
        balances = balance_service.get_wallet_balances(wallet_address)
        return balances
        
    except ValueError as ve:
        raise HTTPException(status_code=404, detail="Wallet not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
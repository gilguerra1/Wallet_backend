# coding: utf-8
import os
import secrets
import hashlib
from typing import Optional, Dict, Any, List
from datetime import datetime

from sqlalchemy import text
from database.connection import get_connection

class WalletRepository:
    
    def createWallet(self) -> Dict[str, Any]:
        """
        Generates public key, private key, saves to database (only private key hash)
        and returns wallet data + private key in plain text.
        """
      
        private_key_size: int = int(os.getenv("PRIVATE_KEY_SIZE", "32")) 
        public_key_size: int = int(os.getenv("PUBLIC_KEY_SIZE", "32"))    
        private_key = secrets.token_hex(private_key_size)               
        address = secrets.token_hex(public_key_size)                     
        private_key_hash = hashlib.sha256(private_key.encode()).hexdigest()

        creation_date = datetime.utcnow()
        initial_status = "ATIVA"

        with get_connection() as conn:
            conn.execute(
                text("""
                    INSERT INTO wallet (wallet_address, private_key_hash, creation_date, status)
                    VALUES (:address, :private_key_hash, :creation_date, :status)
                """),
                {
                    "address": address, 
                    "private_key_hash": private_key_hash,
                    "creation_date": creation_date,
                    "status": initial_status
                },
            )

            row = conn.execute(
                text("""
                    SELECT wallet_address,
                           private_key_hash,
                           creation_date,
                           status
                      FROM wallet
                     WHERE wallet_address = :address
                """),
                {"address": address},
            ).mappings().first()

        wallet = dict(row)
        wallet["private_key"] = private_key
        
        # Create initial balances for all currencies
        from app.repositories.wallet_balance_repos import WalletBalanceRepository
        balance_repo = WalletBalanceRepository()
        balance_repo.create_initial_balances(address)
        
        return wallet
    
    def get_wallet_by_address(self, wallet_address: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a wallet by its address.
        """
        with get_connection() as conn:
            row = conn.execute(
                text("""
                    SELECT wallet_address,
                           private_key_hash,
                           creation_date,
                           status
                      FROM wallet
                     WHERE wallet_address = :address
                """),
                {"address": wallet_address},
            ).mappings().first()

        if row:
            return dict(row)
        return None
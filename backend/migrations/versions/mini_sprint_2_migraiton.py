# -*- coding: utf-8 -*-
"""Initial migration

Revision ID: mini_sprint_2
Revises: 
Create Date: 2025-11-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'mini_sprint_2'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():

    op.execute("""
        CREATE TABLE IF NOT EXISTS currency (
            currency_id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            code VARCHAR(10) NOT NULL UNIQUE,
            type_currency VARCHAR(20) NOT NULL DEFAULT 'fiat'
        )
    """)
    
    # Create wallet table
    op.execute("""
     CREATE TABLE IF NOT EXISTS wallet (
            wallet_address VARCHAR(64) PRIMARY KEY,
            private_key_hash VARCHAR(64) NOT NULL,
            creation_date TIMESTAMP NOT NULL,
            status VARCHAR(15) NOT NULL)
               """)
    
    op.execute("""
    CREATE TABLE IF NOT EXISTS wallet_balance (
            wallet_address VARCHAR(64) NOT NULL,
            currency_id INTEGER NOT NULL,
            PRIMARY KEY (wallet_address, currency_id),
            
            balance DECIMAL(19, 8) NOT NULL DEFAULT 0.0,
            update_date TIMESTAMP NOT NULL,
            
            FOREIGN KEY (wallet_address) REFERENCES wallet (wallet_address),
            FOREIGN KEY (currency_id) REFERENCES currency (currency_id))
    """)

    op.execute("""
    INSERT INTO currency (name, code, type_currency) VALUES
                    ('Bitcoin', 'BTC', 'crypto'),
                    ('Ethereum', 'ETH', 'crypto'),
                    ('Solana', 'SOL', 'crypto'),
                    ('US Dollar', 'USD', 'fiat'),
                    ('Real Brasileiro', 'BRL', 'fiat')
    """)

def downgrade():
    op.execute("DROP TABLE IF EXISTS wallet_balance CASCADE")
    op.execute("DROP TABLE IF EXISTS wallet CASCADE")
    op.execute("DROP TABLE IF EXISTS currency CASCADE")
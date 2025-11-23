from alembic import op

revision = 'mini_sprint_5'
down_revision = 'mini_sprint_4'
branch_labels = None
depends_on = None


def upgrade():

    op.execute("""
    CREATE TABLE IF NOT EXISTS transfer (
        transfer_id BIGSERIAL PRIMARY KEY,

        wallet_origin_address VARCHAR(64) NOT NULL,
        wallet_target_address VARCHAR(64) NOT NULL,

        currency_id SMALLINT NOT NULL,

        value DECIMAL(19, 8) NOT NULL,
        fee_value DECIMAL(19, 8) NOT NULL,
        transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (wallet_origin_address) REFERENCES wallet (wallet_address),
        FOREIGN KEY (wallet_target_address) REFERENCES wallet (wallet_address),
        FOREIGN KEY (currency_id) REFERENCES currency (currency_id)
    );
    """)

    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_transfer_origin_wallet
    ON transfer (wallet_origin_address);
    """)

    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_transfer_target_wallet
    ON transfer (wallet_target_address);
    """)


def downgrade():
    op.execute("DROP TABLE IF EXISTS transfer CASCADE")

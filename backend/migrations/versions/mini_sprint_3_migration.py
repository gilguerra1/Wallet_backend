from alembic import op

revision = 'mini_sprint_3'
down_revision = 'mini_sprint_2'
branch_labels = None
depends_on = None


def upgrade():

    op.execute("""
        CREATE TABLE IF NOT EXISTS deposit_withdrawal (
            movement_id BIGSERIAL PRIMARY KEY,
            wallet_address VARCHAR(64) NOT NULL,
            currency_id SMALLINT NOT NULL,

            transaction_type VARCHAR(10) NOT NULL, -- DEPOSITO ou SAQUE
            value DECIMAL(19, 8) NOT NULL,
            fee_value DECIMAL(19, 8) NOT NULL DEFAULT 0.0,
            transaction_date TIMESTAMP NOT NULL,

            FOREIGN KEY (wallet_address) REFERENCES wallet (wallet_address),
            FOREIGN KEY (currency_id) REFERENCES currency (currency_id)
        );
    """)


def downgrade():
    op.execute("DROP TABLE IF EXISTS deposit_withdrawal CASCADE")

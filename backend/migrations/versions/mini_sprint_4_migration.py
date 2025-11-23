from alembic import op

revision = 'mini_sprint_4'
down_revision = 'mini_sprint_3'
branch_labels = None
depends_on = None


def upgrade():

    op.execute("""
    CREATE TABLE IF NOT EXISTS conversion (
        conversion_id BIGSERIAL PRIMARY KEY,
        wallet_address VARCHAR(64) NOT NULL,

        source_currency_id SMALLINT NOT NULL,
        target_currency_id SMALLINT NOT NULL,

        source_value DECIMAL(19, 8) NOT NULL,
        target_value DECIMAL(19, 8) NOT NULL,

        fee_percentage DECIMAL(5, 4) NOT NULL,
        fee_value DECIMAL(19, 8) NOT NULL,
        used_quotation DECIMAL(20, 8) NOT NULL,
        transaction_date TIMESTAMP NOT NULL,

        FOREIGN KEY (wallet_address) REFERENCES wallet (wallet_address),
        FOREIGN KEY (source_currency_id) REFERENCES currency (currency_id),
        FOREIGN KEY (target_currency_id) REFERENCES currency (currency_id)
    );
    """)


def downgrade():
    op.execute("DROP TABLE IF EXISTS conversion CASCADE")

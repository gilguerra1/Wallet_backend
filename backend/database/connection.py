import os
from pathlib import Path
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)


def get_database_url() -> str:
    db_driver = os.getenv("DB_DRIVER")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME")

    if not all([db_driver, db_user, db_password, db_name]):
        raise ValueError(
            "Database configuration is incomplete in environment variables.")

    return (
        f"{db_driver}://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )


DATABASE_URL = get_database_url()

engine: Engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True)


@contextmanager
def get_connection() -> Connection:

    conn: Connection = engine.connect()
    trans = conn.begin()
    try:
        yield conn
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    finally:
        conn.close()

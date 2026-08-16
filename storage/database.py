import os

import psycopg
from psycopg import Connection


def get_connection() -> Connection:
    """Create and return a PostgreSQL database connection."""
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def create_candles_table() -> None:
    """Create the candles table if it does not already exist."""
    query = """
        CREATE TABLE IF NOT EXISTS candles (
            exchange VARCHAR(20) NOT NULL,
            market_type VARCHAR(20) NOT NULL,
            symbol VARCHAR(30) NOT NULL,
            interval VARCHAR(10) NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL,
            open DOUBLE PRECISION NOT NULL,
            high DOUBLE PRECISION NOT NULL,
            low DOUBLE PRECISION NOT NULL,
            close DOUBLE PRECISION NOT NULL,
            volume DOUBLE PRECISION NOT NULL,
            PRIMARY KEY (
                exchange,
                market_type,
                symbol,
                interval,
                timestamp
            )
        );
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)


def create_trades_table() -> None:
    """Create the trades table if it does not already exist."""
    query = """
        CREATE TABLE IF NOT EXISTS trades (
            exchange VARCHAR(20) NOT NULL,
            market_type VARCHAR(20) NOT NULL,
            symbol VARCHAR(30) NOT NULL,
            trade_id BIGINT NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL,
            price DOUBLE PRECISION NOT NULL,
            quantity DOUBLE PRECISION NOT NULL,
            quote_value DOUBLE PRECISION NOT NULL,
            side VARCHAR(10) NOT NULL,
            PRIMARY KEY (
                exchange,
                market_type,
                symbol,
                trade_id
            )
        );
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)

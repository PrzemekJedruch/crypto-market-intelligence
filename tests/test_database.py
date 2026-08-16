import os
from unittest.mock import patch

from unittest.mock import MagicMock

from storage.database import (
    create_candles_table,
    create_trades_table,
    get_connection,
)


def test_get_connection_uses_environment_variables():
    """Test that get_connection uses PostgreSQL environment variables."""
    environment = {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "crypto_market",
        "DB_USER": "crypto_app",
        "DB_PASSWORD": "test_password",
    }

    with patch.dict(os.environ, environment, clear=True):
        with patch("storage.database.psycopg.connect") as mock_connect:
            get_connection()

    mock_connect.assert_called_once_with(
        host="localhost",
        port="5432",
        dbname="crypto_market",
        user="crypto_app",
        password="test_password",
    )


def test_create_candles_table_executes_create_table_query():
    """Test that create_candles_table executes the candles table SQL."""
    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    with patch(
        "storage.database.get_connection",
        return_value=mock_connection,
    ):
        mock_connection.__enter__.return_value = mock_connection

        create_candles_table()

    executed_query = mock_cursor.execute.call_args.args[0]

    assert "CREATE TABLE IF NOT EXISTS candles" in executed_query
    assert "PRIMARY KEY" in executed_query
    assert "TIMESTAMPTZ" in executed_query
    assert "DOUBLE PRECISION" in executed_query


def test_create_trades_table_executes_create_table_query():
    """Test that create_trades_table executes the trades table SQL."""
    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    with patch(
        "storage.database.get_connection",
        return_value=mock_connection,
    ):
        mock_connection.__enter__.return_value = mock_connection

        create_trades_table()

    executed_query = mock_cursor.execute.call_args.args[0]

    assert "CREATE TABLE IF NOT EXISTS trades" in executed_query
    assert "trade_id BIGINT NOT NULL" in executed_query
    assert "TIMESTAMPTZ" in executed_query
    assert "DOUBLE PRECISION" in executed_query
    assert "PRIMARY KEY" in executed_query

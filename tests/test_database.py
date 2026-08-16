import os
from unittest.mock import patch

from storage.database import get_connection


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
    
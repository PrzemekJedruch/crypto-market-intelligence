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
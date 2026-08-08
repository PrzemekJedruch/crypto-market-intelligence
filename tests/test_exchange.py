from enums.exchange import Exchange
from exchanges.base_exchange import BaseExchange
from datetime import datetime, timedelta, timezone
import pytest

def test_base_exchange_creation():
    """Test that BaseExchange stores the exchange identifier correctly."""
    exchange_client = BaseExchange(exchange=Exchange.BINANCE)

    assert exchange_client.exchange == Exchange.BINANCE


def test_normalize_timestamp_keeps_utc():
    """Test that a UTC timestamp remains in UTC."""
    timestamp = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    normalized = BaseExchange._normalize_timestamp(timestamp)

    assert normalized == timestamp
    assert normalized.tzinfo == timezone.utc


def test_normalize_timestamp_converts_to_utc():
    """Test that a timezone-aware timestamp is converted to UTC."""
    local_timezone = timezone(timedelta(hours=2))
    timestamp = datetime(2026, 1, 1, 14, 0, tzinfo=local_timezone)

    normalized = BaseExchange._normalize_timestamp(timestamp)

    assert normalized == datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    assert normalized.tzinfo == timezone.utc


def test_normalize_timestamp_rejects_naive_datetime():
    """Test that a naive datetime without timezone information is rejected."""
    timestamp = datetime(2026, 1, 1, 12, 0)

    with pytest.raises(ValueError, match="Timestamp must be timezone-aware."):
        BaseExchange._normalize_timestamp(timestamp)
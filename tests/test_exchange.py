from enums.exchange import Exchange
from exchanges.base_exchange import BaseExchange
from datetime import datetime, timedelta, timezone
import pytest
from exchanges.binance import BinanceExchange
from unittest.mock import patch


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

def test_normalize_symbol():
    """Test that a symbol is normalized to uppercase without surrounding spaces."""
    symbol = " ethusdt "

    normalized = BaseExchange._normalize_symbol(symbol)

    assert normalized == "ETHUSDT"

def test_normalize_symbol_rejects_invalid_format():
    """Test that symbols with separators are rejected."""
    symbol = "BTC-USDT"

    with pytest.raises(ValueError, match="Symbol must contain only letters and numbers."):
        BaseExchange._normalize_symbol(symbol)

def test_normalize_symbol_rejects_empty_symbol():
    """Test that an empty symbol is rejected."""
    symbol = "   "

    with pytest.raises(ValueError, match="Symbol cannot be empty."):
        BaseExchange._normalize_symbol(symbol)

def test_binance_exchange_creation():
    """Test that BinanceExchange uses the Binance exchange identifier and base URL."""
    exchange_client = BinanceExchange()

    # Verify inheritance
    assert isinstance(exchange_client, BaseExchange)

    # Verify Binance-specific configuration
    assert exchange_client.exchange == Exchange.BINANCE
    assert exchange_client.BASE_URL == "https://fapi.binance.com"


@patch("exchanges.binance.requests.get")
def test_binance_ping(mock_get):
    """Test that BinanceExchange sends a request to the Binance ping endpoint."""
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None

    exchange_client = BinanceExchange()

    result = exchange_client.ping()

    assert result is True

    mock_get.assert_called_once_with(
        "https://fapi.binance.com/fapi/v1/ping",
        timeout=10,
    )

    mock_response.raise_for_status.assert_called_once_with()

def test_get_candles_raw():
    """Test that BinanceExchange requests raw candle data correctly."""
    raw_candles = [
        [
            1720000000000,
            "60000.0",
            "60100.0",
            "59900.0",
            "60050.0",
            "12.5",
        ]
    ]

    with patch("exchanges.binance.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = raw_candles
        mock_response.raise_for_status.return_value = None

        exchange_client = BinanceExchange()

        result = exchange_client._get_candles_raw(
            symbol="btcusdt",
            interval="1m",
            limit=5,
        )

        assert result == raw_candles

        mock_get.assert_called_once_with(
            "https://fapi.binance.com/fapi/v1/klines",
            params={
                "symbol": "BTCUSDT",
                "interval": "1m",
                "limit": 5,
            },
            timeout=10,
        )

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()


def test_get_trades_raw():
    """Test that BinanceExchange requests raw aggregate trade data correctly."""
    raw_trades = [
        {
            "a": 12345,
            "p": "63450.10",
            "q": "0.125",
            "f": 100,
            "l": 101,
            "T": 1786637160000,
            "m": False,
        }
    ]

    with patch("exchanges.binance.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = raw_trades
        mock_response.raise_for_status.return_value = None

        exchange_client = BinanceExchange()

        result = exchange_client._get_trades_raw(
            symbol="btcusdt",
            limit=5,
        )

        assert result == raw_trades

        mock_get.assert_called_once_with(
            "https://fapi.binance.com/fapi/v1/aggTrades",
            params={
                "symbol": "BTCUSDT",
                "limit": 5,
            },
            timeout=10,
        )

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()

def test_get_open_interest_raw():
    """Test that BinanceExchange requests raw Open Interest data correctly."""
    raw_open_interest = [
        {
            "symbol": "BTCUSDT",
            "sumOpenInterest": "12345.67",
            "sumOpenInterestValue": "987654321.00",
            "timestamp": 1786639477827,
        }
    ]

    with patch("exchanges.binance.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = raw_open_interest
        mock_response.raise_for_status.return_value = None

        exchange_client = BinanceExchange()

        result = exchange_client._get_open_interest_raw(
            symbol="btcusdt",
            period="5m",
            limit=5,
        )

        assert result == raw_open_interest

        mock_get.assert_called_once_with(
            "https://fapi.binance.com/futures/data/openInterestHist",
            params={
                "symbol": "BTCUSDT",
                "period": "5m",
                "limit": 5,
            },
            timeout=10,
        )

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()

def test_get_funding_rate_raw():
    """Test that BinanceExchange requests raw funding rate data correctly."""
    raw_funding_rates = [
        {
            "symbol": "BTCUSDT",
            "fundingTime": 1786646400000,
            "fundingRate": "0.00010000",
            "markPrice": "63125.40",
        }
    ]

    with patch("exchanges.binance.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = raw_funding_rates
        mock_response.raise_for_status.return_value = None

        exchange_client = BinanceExchange()

        result = exchange_client._get_funding_rate_raw(
            symbol="btcusdt",
            limit=5,
        )

        assert result == raw_funding_rates

        mock_get.assert_called_once_with(
            "https://fapi.binance.com/fapi/v1/fundingRate",
            params={
                "symbol": "BTCUSDT",
                "limit": 5,
            },
            timeout=10,
        )

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()

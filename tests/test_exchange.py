from enums.exchange import Exchange
from enums.trade_side import TradeSide
from exchanges.base_exchange import BaseExchange
from datetime import datetime, timedelta, timezone
import pytest
from exchanges.binance import BinanceExchange
from unittest.mock import patch
from enums.market_type import MarketType
from models.open_interest import OpenInterest


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

def test_get_candles_raw_with_time_range():
    """Test that BinanceExchange includes start and end times in candle requests."""
    raw_candles = []

    with patch("exchanges.binance.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = raw_candles
        mock_response.raise_for_status.return_value = None

        exchange_client = BinanceExchange()

        result = exchange_client._get_candles_raw(
            symbol="btcusdt",
            interval="1m",
            limit=5,
            start_time=1786637160000,
            end_time=1786637460000,
        )

        assert result == raw_candles

        mock_get.assert_called_once_with(
            "https://fapi.binance.com/fapi/v1/klines",
            params={
                "symbol": "BTCUSDT",
                "interval": "1m",
                "limit": 5,
                "startTime": 1786637160000,
                "endTime": 1786637460000,
            },
            timeout=10,
        )

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()

    
def test_get_candles_returns_normalized_models():
    """Test that BinanceExchange converts raw candles into Candle models."""
    raw_candles = [
        [
            1786637160000,
            "63465.00",
            "63484.10",
            "63431.00",
            "63431.10",
            "149.946",
        ]
    ]

    with patch.object(
        BinanceExchange,
        "_get_candles_raw",
        return_value=raw_candles,
    ) as mock_get_candles_raw:
        exchange_client = BinanceExchange()

        start_time = datetime(
            2026,
            8,
            13,
            10,
            0,
            tzinfo=timezone.utc,
        )
        end_time = datetime(
            2026,
            8,
            13,
            11,
            0,
            tzinfo=timezone.utc,
        )

        result = exchange_client.get_candles(
            symbol="btcusdt",
            market_type=MarketType.PERPETUAL,
            interval="1m",
            start_time=start_time,
            end_time=end_time,
        )

        assert len(result) == 1

        candle = result[0]

        assert candle.exchange == Exchange.BINANCE
        assert candle.market_type == MarketType.PERPETUAL
        assert candle.symbol == "BTCUSDT"
        assert candle.interval == "1m"
        assert candle.open == 63465.0
        assert candle.high == 63484.1
        assert candle.low == 63431.0
        assert candle.close == 63431.1
        assert candle.volume == 149.946
        assert candle.timestamp == datetime.fromtimestamp(
            1786637160000 / 1000,
            tz=timezone.utc,
        )

        mock_get_candles_raw.assert_called_once_with(
            symbol="BTCUSDT",
            interval="1m",
            start_time=int(start_time.timestamp() * 1000),
            end_time=int(end_time.timestamp() * 1000),
        )
def test_get_trades_raw_with_time_range():
    """Test that BinanceExchange includes start and end times in trade requests."""
    raw_trades = []

    with patch("exchanges.binance.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = raw_trades
        mock_response.raise_for_status.return_value = None

        exchange_client = BinanceExchange()

        result = exchange_client._get_trades_raw(
            symbol="btcusdt",
            limit=5,
            start_time=1786637160000,
            end_time=1786637460000,
        )

        assert result == raw_trades

        mock_get.assert_called_once_with(
            "https://fapi.binance.com/fapi/v1/aggTrades",
            params={
                "symbol": "BTCUSDT",
                "limit": 5,
                "startTime": 1786637160000,
                "endTime": 1786637460000,
            },
            timeout=10,
        )

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()

def test_get_trades_returns_normalized_models():
    """Test that BinanceExchange converts raw trades into Trade models."""
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

    with patch.object(
        BinanceExchange,
        "_get_trades_raw",
        return_value=raw_trades,
    ) as mock_get_trades_raw:
        exchange_client = BinanceExchange()

        start_time = datetime(
            2026,
            8,
            13,
            10,
            0,
            tzinfo=timezone.utc,
        )
        end_time = datetime(
            2026,
            8,
            13,
            10,
            30,
            tzinfo=timezone.utc,
        )

        result = exchange_client.get_trades(
            symbol="btcusdt",
            market_type=MarketType.PERPETUAL,
            start_time=start_time,
            end_time=end_time,
        )

        assert len(result) == 1

        trade = result[0]

        assert trade.exchange == Exchange.BINANCE
        assert trade.market_type == MarketType.PERPETUAL
        assert trade.symbol == "BTCUSDT"
        assert trade.trade_id == 12345
        assert trade.price == 63450.10
        assert trade.quantity == 0.125
        assert trade.quote_value == 63450.10 * 0.125
        assert trade.side == TradeSide.BUY
        assert trade.timestamp == datetime.fromtimestamp(
            1786637160000 / 1000,
            tz=timezone.utc,
        )

        mock_get_trades_raw.assert_called_once_with(
            symbol="BTCUSDT",
            start_time=int(start_time.timestamp() * 1000),
            end_time=int(end_time.timestamp() * 1000),
        )

def test_get_open_interest_raw_with_time_range():
    """Test that BinanceExchange includes start and end times in Open Interest requests."""
    raw_open_interest = []

    with patch("exchanges.binance.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = raw_open_interest
        mock_response.raise_for_status.return_value = None

        exchange_client = BinanceExchange()

        result = exchange_client._get_open_interest_raw(
            symbol="btcusdt",
            period="5m",
            limit=5,
            start_time=1786637160000,
            end_time=1786637460000,
        )

        assert result == raw_open_interest

        mock_get.assert_called_once_with(
            "https://fapi.binance.com/futures/data/openInterestHist",
            params={
                "symbol": "BTCUSDT",
                "period": "5m",
                "limit": 5,
                "startTime": 1786637160000,
                "endTime": 1786637460000,
            },
            timeout=10,
        )

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()

def test_get_open_interest_returns_normalized_models():
    """Test that BinanceExchange converts raw Open Interest into models."""
    raw_open_interest = [
        {
            "symbol": "BTCUSDT",
            "sumOpenInterest": "109816.19100000",
            "sumOpenInterestValue": "6921956114.35020000",
            "CMCCirculatingSupply": "20069371.00000000",
            "timestamp": 1786640100000,
        }
    ]

    with patch.object(
        BinanceExchange,
        "_get_open_interest_raw",
        return_value=raw_open_interest,
    ) as mock_get_open_interest_raw:
        exchange_client = BinanceExchange()

        start_time = datetime(
            2026,
            8,
            13,
            10,
            0,
            tzinfo=timezone.utc,
        )
        end_time = datetime(
            2026,
            8,
            13,
            11,
            0,
            tzinfo=timezone.utc,
        )

        result = exchange_client.get_open_interest(
            symbol="btcusdt",
            market_type=MarketType.PERPETUAL,
            start_time=start_time,
            end_time=end_time,
        )

        assert len(result) == 1

        open_interest = result[0]

        assert isinstance(open_interest, OpenInterest)
        assert open_interest.exchange == Exchange.BINANCE
        assert open_interest.market_type == MarketType.PERPETUAL
        assert open_interest.symbol == "BTCUSDT"
        assert open_interest.open_interest == 109816.191
        assert open_interest.open_interest_usd == 6921956114.3502
        assert open_interest.timestamp == datetime.fromtimestamp(
            1786640100000 / 1000,
            tz=timezone.utc,
        )

        mock_get_open_interest_raw.assert_called_once_with(
            symbol="BTCUSDT",
            period="5m",
            start_time=int(start_time.timestamp() * 1000),
            end_time=int(end_time.timestamp() * 1000),
        )

def test_get_funding_rate_raw_with_time_range():
    """Test that BinanceExchange includes start and end times in funding-rate requests."""
    raw_funding_rates = []

    with patch("exchanges.binance.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = raw_funding_rates
        mock_response.raise_for_status.return_value = None

        exchange_client = BinanceExchange()

        result = exchange_client._get_funding_rate_raw(
            symbol="btcusdt",
            limit=5,
            start_time=1786521600000,
            end_time=1786636800000,
        )

        assert result == raw_funding_rates

        mock_get.assert_called_once_with(
            "https://fapi.binance.com/fapi/v1/fundingRate",
            params={
                "symbol": "BTCUSDT",
                "limit": 5,
                "startTime": 1786521600000,
                "endTime": 1786636800000,
            },
            timeout=10,
        )

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()

def test_get_funding_rate_returns_normalized_models():
    """Test that BinanceExchange converts raw funding rates into FundingRate models."""
    raw_funding_rates = [
        {
            "symbol": "BTCUSDT",
            "fundingTime": 1786521600000,
            "fundingRate": "0.00008568",
            "markPrice": "63810.89568841",
            "rateType": "Regular",
        }
    ]

    with patch.object(
        BinanceExchange,
        "_get_funding_rate_raw",
        return_value=raw_funding_rates,
    ) as mock_get_funding_rate_raw:
        exchange_client = BinanceExchange()

        start_time = datetime(
            2026,
            8,
            13,
            0,
            0,
            tzinfo=timezone.utc,
        )
        end_time = datetime(
            2026,
            8,
            13,
            8,
            0,
            tzinfo=timezone.utc,
        )

        result = exchange_client.get_funding_rate(
            symbol="btcusdt",
            market_type=MarketType.PERPETUAL,
            start_time=start_time,
            end_time=end_time,
        )

        assert len(result) == 1

        funding_rate = result[0]

        assert funding_rate.exchange == Exchange.BINANCE
        assert funding_rate.market_type == MarketType.PERPETUAL
        assert funding_rate.symbol == "BTCUSDT"
        assert funding_rate.funding_rate == 0.00008568
        assert funding_rate.next_funding_time is None
        assert funding_rate.timestamp == datetime.fromtimestamp(
            1786521600000 / 1000,
            tz=timezone.utc,
        )

        mock_get_funding_rate_raw.assert_called_once_with(
            symbol="BTCUSDT",
            start_time=int(start_time.timestamp() * 1000),
            end_time=int(end_time.timestamp() * 1000),
        )
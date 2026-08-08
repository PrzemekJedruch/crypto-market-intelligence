from datetime import datetime, timezone

from enums.exchange import Exchange
from enums.market_type import MarketType
from models.base_market_data import BaseMarketData
from models.candle import Candle
from enums.trade_side import TradeSide
from models.trade import Trade
from models.open_interest import OpenInterest
from models.funding_rate import FundingRate


def test_base_market_data_creation():
    """Test that BaseMarketData stores all common market data fields correctly."""
    timestamp = datetime.now(timezone.utc)

    market_data = BaseMarketData(
        exchange=Exchange.BINANCE,
        market_type=MarketType.PERPETUAL,
        symbol="BTCUSDT",
        timestamp=timestamp,
    )

    # Verify common market data fields
    assert market_data.exchange == Exchange.BINANCE
    assert market_data.market_type == MarketType.PERPETUAL
    assert market_data.symbol == "BTCUSDT"
    assert market_data.timestamp == timestamp


def test_candle_creation_and_inheritance():
    """Test that Candle stores its fields and inherits from BaseMarketData."""
    timestamp = datetime.now(timezone.utc)

    candle = Candle(
        exchange=Exchange.BINANCE,
        market_type=MarketType.PERPETUAL,
        symbol="BTCUSDT",
        timestamp=timestamp,
        interval="1m",
        open=100.0,
        high=110.0,
        low=95.0,
        close=105.0,
        volume=250.0,
    )

    # Verify inheritance
    assert isinstance(candle, BaseMarketData)

    # Verify inherited fields
    assert candle.exchange == Exchange.BINANCE
    assert candle.market_type == MarketType.PERPETUAL
    assert candle.symbol == "BTCUSDT"
    assert candle.timestamp == timestamp

    # Verify Candle-specific fields
    assert candle.interval == "1m"
    assert candle.open == 100.0
    assert candle.high == 110.0
    assert candle.low == 95.0
    assert candle.close == 105.0
    assert candle.volume == 250.0



def test_trade_creation_and_inheritance():
    """Test that Trade stores its fields and inherits from BaseMarketData."""
    timestamp = datetime.now(timezone.utc)

    trade = Trade(
        exchange=Exchange.BINANCE,
        market_type=MarketType.PERPETUAL,
        symbol="BTCUSDT",
        timestamp=timestamp,
        trade_id=123456,
        price=100000.0,
        quantity=0.25,
        quote_value=25000.0,
        side=TradeSide.BUY,
    )

    # Verify inheritance
    assert isinstance(trade, BaseMarketData)

    # Verify inherited fields
    assert trade.exchange == Exchange.BINANCE
    assert trade.market_type == MarketType.PERPETUAL
    assert trade.symbol == "BTCUSDT"
    assert trade.timestamp == timestamp

    # Verify Trade-specific fields
    assert trade.trade_id == 123456
    assert trade.price == 100000.0
    assert trade.quantity == 0.25
    assert trade.quote_value == 25000.0
    assert trade.side == TradeSide.BUY

def test_open_interest_creation_and_inheritance():
    """Test that OpenInterest stores its fields and inherits from BaseMarketData."""
    timestamp = datetime.now(timezone.utc)

    open_interest = OpenInterest(
        exchange=Exchange.BINANCE,
        market_type=MarketType.PERPETUAL,
        symbol="BTCUSDT",
        timestamp=timestamp,
        open_interest=12500.0,
        open_interest_usd=1250000000.0,
    )

    # Verify inheritance
    assert isinstance(open_interest, BaseMarketData)

    # Verify inherited fields
    assert open_interest.exchange == Exchange.BINANCE
    assert open_interest.market_type == MarketType.PERPETUAL
    assert open_interest.symbol == "BTCUSDT"
    assert open_interest.timestamp == timestamp

    # Verify OpenInterest-specific fields
    assert open_interest.open_interest == 12500.0
    assert open_interest.open_interest_usd == 1250000000.0


def test_funding_rate_creation_and_inheritance():
    """Test that FundingRate stores its fields and inherits from BaseMarketData."""
    timestamp = datetime.now(timezone.utc)
    next_funding_time = datetime.now(timezone.utc)

    funding_rate = FundingRate(
        exchange=Exchange.BINANCE,
        market_type=MarketType.PERPETUAL,
        symbol="BTCUSDT",
        timestamp=timestamp,
        funding_rate=0.0001,
        next_funding_time=next_funding_time,
    )

    # Verify inheritance
    assert isinstance(funding_rate, BaseMarketData)

    # Verify inherited fields
    assert funding_rate.exchange == Exchange.BINANCE
    assert funding_rate.market_type == MarketType.PERPETUAL
    assert funding_rate.symbol == "BTCUSDT"
    assert funding_rate.timestamp == timestamp

    # Verify FundingRate-specific fields
    assert funding_rate.funding_rate == 0.0001
    assert funding_rate.next_funding_time == next_funding_time


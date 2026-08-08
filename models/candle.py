from dataclasses import dataclass
from datetime import datetime

from enums.exchange import Exchange
from enums.market_type import MarketType


@dataclass
class Candle:
    # Exchange from which the candle data comes
    exchange: Exchange

    # Type of market, for example spot or perpetual
    market_type: MarketType

    # Trading symbol, for example BTCUSDT
    symbol: str

    # Candle interval, for example 1m, 5m, 1h
    interval: str

    # Opening time of the candle
    timestamp: datetime

    # OHLC price data
    open: float
    high: float
    low: float
    close: float

    # Trading volume during the candle period
    volume: float
    
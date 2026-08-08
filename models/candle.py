from dataclasses import dataclass

from models.base_market_data import BaseMarketData


@dataclass
class Candle(BaseMarketData):
    # Candle interval, for example 1m, 5m, or 1h
    interval: str

    # OHLC price data
    open: float
    high: float
    low: float
    close: float

    # Trading volume during the candle period
    volume: float
    
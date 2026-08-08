from dataclasses import dataclass
from datetime import datetime

from enums.exchange import Exchange
from enums.market_type import MarketType


@dataclass
class BaseMarketData:
    # Exchange from which the market data comes
    exchange: Exchange

    # Type of market, for example spot, perpetual, or futures
    market_type: MarketType

    # Trading symbol, for example BTCUSDT
    symbol: str

    # Timestamp of the market data record in UTC
    timestamp: datetime

    
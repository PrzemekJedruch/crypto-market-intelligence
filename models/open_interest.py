from dataclasses import dataclass
from datetime import datetime

from enums.exchange import Exchange
from enums.market_type import MarketType


@dataclass
class OpenInterest:
    # Exchange from which the open interest data comes
    exchange: Exchange

    # Type of market, usually perpetual or futures
    market_type: MarketType

    # Trading symbol, for example BTCUSDT
    symbol: str

    # Time of the open interest measurement
    timestamp: datetime

    # Open interest value in the unit provided by the exchange
    open_interest: float

    # Open interest converted to USD or USDT value
    open_interest_usd: float
    
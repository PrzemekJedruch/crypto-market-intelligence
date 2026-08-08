from dataclasses import dataclass
from datetime import datetime

from enums.exchange import Exchange
from enums.market_type import MarketType


@dataclass
class FundingRate:
    # Exchange from which the funding rate data comes
    exchange: Exchange

    # Type of market, usually perpetual
    market_type: MarketType

    # Trading symbol, for example BTCUSDT
    symbol: str

    # Time when the funding rate was recorded
    timestamp: datetime

    # Funding rate value
    funding_rate: float

    # Time of the next scheduled funding payment
    next_funding_time: datetime | None = None
    
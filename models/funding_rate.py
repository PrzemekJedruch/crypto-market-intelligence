from dataclasses import dataclass
from datetime import datetime

from models.base_market_data import BaseMarketData


@dataclass
class FundingRate(BaseMarketData):
    # Funding rate value
    funding_rate: float

    # Time of the next scheduled funding payment
    next_funding_time: datetime | None = None

    
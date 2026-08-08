from dataclasses import dataclass

from models.base_market_data import BaseMarketData


@dataclass
class OpenInterest(BaseMarketData):
    # Open interest value in the unit provided by the exchange
    open_interest: float

    # Open interest converted to USD or USDT
    open_interest_usd: float

    
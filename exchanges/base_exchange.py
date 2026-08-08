from datetime import datetime, timezone

from enums.exchange import Exchange
from enums.market_type import MarketType
from models.candle import Candle
from models.trade import Trade
from models.open_interest import OpenInterest
from models.funding_rate import FundingRate


class BaseExchange:
    """Base class for cryptocurrency exchange clients.

    All timestamps passed to and returned by exchange clients must use UTC.
    """
    def __init__(self, exchange: Exchange):
        """Initialize the exchange client."""
        self.exchange = exchange

    def get_candles(
        self,
        symbol: str,
        market_type: MarketType,
        interval: str,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Candle]:
        """Return normalized candle data for the requested time range."""
        raise NotImplementedError

    def get_trades(
        self,
        symbol: str,
        market_type: MarketType,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Trade]:
        """Return normalized trade data for the requested time range."""
        raise NotImplementedError

    def get_open_interest(
        self,
        symbol: str,
        market_type: MarketType,
        start_time: datetime,
        end_time: datetime,
    ) -> list[OpenInterest]:
        """Return normalized open interest data for the requested time range."""
        raise NotImplementedError

    def get_funding_rate(
        self,
        symbol: str,
        market_type: MarketType,
        start_time: datetime,
        end_time: datetime,
    ) -> list[FundingRate]:
        """Return normalized funding rate data for the requested time range."""
        raise NotImplementedError

    def get_supported_symbols(
        self,
        market_type: MarketType,
    ) -> list[str]:
        """Return symbols supported by the exchange for the given market type."""
        raise NotImplementedError

    @staticmethod
    def _normalize_timestamp(timestamp: datetime) -> datetime:
        """Return a timezone-aware datetime normalized to UTC."""
        
        if timestamp.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware.")

        return timestamp.astimezone(timezone.utc)
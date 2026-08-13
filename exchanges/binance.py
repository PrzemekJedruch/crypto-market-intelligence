from datetime import datetime, timezone

import requests

from enums.exchange import Exchange
from enums.market_type import MarketType
from enums.trade_side import TradeSide
from exchanges.base_exchange import BaseExchange
from models.candle import Candle
from models.trade import Trade
from models.open_interest import OpenInterest
from models.funding_rate import FundingRate


class BinanceAPIError(Exception):
    """Raised when a Binance API request fails."""


class BinanceExchange(BaseExchange):
    """Client for Binance USD-M Futures public market data API."""

    BASE_URL = "https://fapi.binance.com"

    def __init__(self):
        """Initialize the Binance exchange client."""
        super().__init__(exchange=Exchange.BINANCE)

    def _get_json(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> list | dict:
        """Send a GET request to Binance and return the decoded JSON response."""
        try:
            response = requests.get(
                f"{self.BASE_URL}{endpoint}",
                params=params,
                timeout=10,
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:
            raise BinanceAPIError(f"Binance API request failed: {error}") from error

    def ping(self) -> bool:
        """Check whether the Binance Futures API is reachable."""
        self._get_json("/fapi/v1/ping")
        return True

    def _get_candles_raw(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
        start_time: int | None = None,
        end_time: int | None = None,
    ) -> list:
        """Download raw candle data from Binance USD-M Futures."""
        normalized_symbol = self._normalize_symbol(symbol)

        params = {
            "symbol": normalized_symbol,
            "interval": interval,
            "limit": limit,
        }

        if start_time is not None:
            params["startTime"] = start_time

        if end_time is not None:
            params["endTime"] = end_time

        return self._get_json(
            endpoint="/fapi/v1/klines",
            params=params,
        )

    def get_candles(
        self,
        symbol: str,
        market_type: MarketType,
        interval: str,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Candle]:
        """Return normalized candle data for the requested time range."""
        normalized_start = self._normalize_timestamp(start_time)
        normalized_end = self._normalize_timestamp(end_time)
        normalized_symbol = self._normalize_symbol(symbol)

        raw_candles = self._get_candles_raw(
            symbol=normalized_symbol,
            interval=interval,
            start_time=int(normalized_start.timestamp() * 1000),
            end_time=int(normalized_end.timestamp() * 1000),
        )

        return [
            Candle(
                exchange=self.exchange,
                market_type=market_type,
                symbol=normalized_symbol,
                timestamp=datetime.fromtimestamp(
                    candle[0] / 1000,
                    tz=timezone.utc,
                ),
                interval=interval,
                open=float(candle[1]),
                high=float(candle[2]),
                low=float(candle[3]),
                close=float(candle[4]),
                volume=float(candle[5]),
            )
            for candle in raw_candles
        ]

    def _get_trades_raw(
        self,
        symbol: str,
        limit: int = 500,
        start_time: int | None = None,
        end_time: int | None = None,
    ) -> list:
        """Download raw aggregate trade data from Binance USD-M Futures."""
        normalized_symbol = self._normalize_symbol(symbol)

        params = {
            "symbol": normalized_symbol,
            "limit": limit,
        }

        if start_time is not None:
            params["startTime"] = start_time

        if end_time is not None:
            params["endTime"] = end_time

        return self._get_json(
            endpoint="/fapi/v1/aggTrades",
            params=params,
        )

    def get_trades(
        self,
        symbol: str,
        market_type: MarketType,
        start_time: datetime,
        end_time: datetime,
    ) -> list[Trade]:
        """Return normalized trade data for the requested time range."""
        normalized_start = self._normalize_timestamp(start_time)
        normalized_end = self._normalize_timestamp(end_time)
        normalized_symbol = self._normalize_symbol(symbol)

        raw_trades = self._get_trades_raw(
            symbol=normalized_symbol,
            start_time=int(normalized_start.timestamp() * 1000),
            end_time=int(normalized_end.timestamp() * 1000),
        )

        return [
            Trade(
                exchange=self.exchange,
                market_type=market_type,
                symbol=normalized_symbol,
                timestamp=datetime.fromtimestamp(
                    trade["T"] / 1000,
                    tz=timezone.utc,
                ),
                trade_id=trade["a"],
                price=float(trade["p"]),
                quantity=float(trade["q"]),
                quote_value=float(trade["p"]) * float(trade["q"]),
                side=TradeSide.SELL if trade["m"] else TradeSide.BUY,
            )
            for trade in raw_trades
        ]

    def _get_open_interest_raw(
        self,
        symbol: str,
        period: str = "5m",
        limit: int = 30,
        start_time: int | None = None,
        end_time: int | None = None,
    ) -> list:
        """Download raw historical Open Interest data from Binance USD-M Futures."""
        normalized_symbol = self._normalize_symbol(symbol)

        params = {
            "symbol": normalized_symbol,
            "period": period,
            "limit": limit,
        }

        if start_time is not None:
            params["startTime"] = start_time

        if end_time is not None:
            params["endTime"] = end_time

        return self._get_json(
            endpoint="/futures/data/openInterestHist",
            params=params,
        )

    def get_open_interest(
        self,
        symbol: str,
        market_type: MarketType,
        start_time: datetime,
        end_time: datetime,
    ) -> list[OpenInterest]:
        """Return normalized Open Interest data for the requested time range."""
        normalized_start = self._normalize_timestamp(start_time)
        normalized_end = self._normalize_timestamp(end_time)
        normalized_symbol = self._normalize_symbol(symbol)

        raw_open_interest = self._get_open_interest_raw(
            symbol=normalized_symbol,
            period="5m",
            start_time=int(normalized_start.timestamp() * 1000),
            end_time=int(normalized_end.timestamp() * 1000),
        )

        return [
            OpenInterest(
                exchange=self.exchange,
                market_type=market_type,
                symbol=normalized_symbol,
                timestamp=datetime.fromtimestamp(
                    record["timestamp"] / 1000,
                    tz=timezone.utc,
                ),
                open_interest=float(record["sumOpenInterest"]),
                open_interest_usd=float(record["sumOpenInterestValue"]),
            )
            for record in raw_open_interest
        ]

    def _get_funding_rate_raw(
        self,
        symbol: str,
        limit: int = 100,
        start_time: int | None = None,
        end_time: int | None = None,
    ) -> list:
        """Download raw historical funding rate data from Binance USD-M Futures."""
        normalized_symbol = self._normalize_symbol(symbol)

        params = {
            "symbol": normalized_symbol,
            "limit": limit,
        }

        if start_time is not None:
            params["startTime"] = start_time

        if end_time is not None:
            params["endTime"] = end_time

        return self._get_json(
            endpoint="/fapi/v1/fundingRate",
            params=params,
        )

    def get_funding_rate(
        self,
        symbol: str,
        market_type: MarketType,
        start_time: datetime,
        end_time: datetime,
    ) -> list[FundingRate]:
        """Return normalized funding rate data for the requested time range."""
        normalized_start = self._normalize_timestamp(start_time)
        normalized_end = self._normalize_timestamp(end_time)
        normalized_symbol = self._normalize_symbol(symbol)

        raw_funding_rates = self._get_funding_rate_raw(
            symbol=normalized_symbol,
            start_time=int(normalized_start.timestamp() * 1000),
            end_time=int(normalized_end.timestamp() * 1000),
        )

        return [
            FundingRate(
                exchange=self.exchange,
                market_type=market_type,
                symbol=normalized_symbol,
                timestamp=datetime.fromtimestamp(
                    record["fundingTime"] / 1000,
                    tz=timezone.utc,
                ),
                funding_rate=float(record["fundingRate"]),
                next_funding_time=None,
            )
            for record in raw_funding_rates
        ]

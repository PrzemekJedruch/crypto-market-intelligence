from urllib import response

import requests

from enums.exchange import Exchange
from exchanges.base_exchange import BaseExchange

from datetime import datetime, timezone

from enums.market_type import MarketType
from models.candle import Candle

from enums.trade_side import TradeSide
from models.trade import Trade


class BinanceExchange(BaseExchange):
    """Client for Binance USD-M Futures public market data API."""

    BASE_URL = "https://fapi.binance.com"

    def __init__(self):
        """Initialize the Binance exchange client."""
        super().__init__(exchange=Exchange.BINANCE)

    def ping(self) -> bool:
        """Check whether the Binance Futures API is reachable."""
        response = requests.get(
            f"{self.BASE_URL}/fapi/v1/ping",
            timeout=10,
        )

        response.raise_for_status()

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

        response = requests.get(
            f"{self.BASE_URL}/fapi/v1/klines",
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

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

        response = requests.get(
            f"{self.BASE_URL}/fapi/v1/aggTrades",
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

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
    ) -> list:
        """Download raw historical Open Interest data from Binance USD-M Futures."""
        normalized_symbol = self._normalize_symbol(symbol)

        response = requests.get(
            f"{self.BASE_URL}/futures/data/openInterestHist",
            params={
                "symbol": normalized_symbol,
                "period": period,
                "limit": limit,
            },
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    def _get_funding_rate_raw(
        self,
        symbol: str,
        limit: int = 100,
    ) -> list:
        """Download raw historical funding rate data from Binance USD-M Futures."""
        normalized_symbol = self._normalize_symbol(symbol)

        response = requests.get(
            f"{self.BASE_URL}/fapi/v1/fundingRate",
            params={
                "symbol": normalized_symbol,
                "limit": limit,
            },
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

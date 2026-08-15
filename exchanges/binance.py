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

    CANDLE_REQUEST_LIMIT = 1000
    TRADE_REQUEST_LIMIT = 1000
    TRADE_REQUEST_WINDOW_MS = 60 * 60 * 1000 - 1

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

        raw_candles = self._get_all_candles_raw(
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
        from_id: int | None = None,
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

        if from_id is not None:
            params["fromId"] = from_id

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

        raw_trades = self._get_all_trades_raw(
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

    @staticmethod
    def _interval_to_milliseconds(interval: str) -> int:
        """Convert a Binance candle interval into milliseconds."""
        interval_map = {
            "1m": 60_000,
            "3m": 180_000,
            "5m": 300_000,
            "15m": 900_000,
            "30m": 1_800_000,
            "1h": 3_600_000,
            "2h": 7_200_000,
            "4h": 14_400_000,
            "6h": 21_600_000,
            "8h": 28_800_000,
            "12h": 43_200_000,
            "1d": 86_400_000,
        }

        try:
            return interval_map[interval]
        except KeyError as error:
            raise ValueError(f"Unsupported candle interval: {interval}") from error

    def _get_all_candles_raw(
        self,
        symbol: str,
        interval: str,
        start_time: int,
        end_time: int,
    ) -> list:
        """Download all raw candles for the requested time range."""
        interval_ms = self._interval_to_milliseconds(interval)
        current_start_time = start_time
        all_candles = []

        while current_start_time <= end_time:
            candles = self._get_candles_raw(
                symbol=symbol,
                interval=interval,
                limit=self.CANDLE_REQUEST_LIMIT,
                start_time=current_start_time,
                end_time=end_time,
            )

            if not candles:
                break

            all_candles.extend(candles)

            last_open_time = candles[-1][0]
            next_start_time = last_open_time + interval_ms

            if next_start_time <= current_start_time:
                break

            current_start_time = next_start_time

            if len(candles) < self.CANDLE_REQUEST_LIMIT:
                break

        return all_candles


    @staticmethod
    def _split_time_range(
        start_time: int,
        end_time: int,
        window_ms: int,
    ) -> list[tuple[int, int]]:
        """Split a millisecond time range into smaller inclusive windows."""
        windows = []
        current_start = start_time

        while current_start <= end_time:
            current_end = min(
                current_start + window_ms,
                end_time,
            )

            windows.append(
                (
                    current_start,
                    current_end,
                )
            )

            current_start = current_end + 1

        return windows
    def _get_all_trades_raw(
        self,
        symbol: str,
        start_time: int,
        end_time: int,
    ) -> list:
        """Download all raw aggregate trades for the requested time range."""
        all_trades = []

        windows = self._split_time_range(
            start_time=start_time,
            end_time=end_time,
            window_ms=self.TRADE_REQUEST_WINDOW_MS,
        )

        for window_start, window_end in windows:
            trades = self._get_trades_window_raw(
                symbol=symbol,
                start_time=window_start,
                end_time=window_end,
            )

            all_trades.extend(trades)

        return all_trades


    def _get_trades_window_raw(
        self,
        symbol: str,
        start_time: int,
        end_time: int,
    ) -> list:
        """Download all raw aggregate trades within one time window."""
        trades = self._get_trades_raw(
            symbol=symbol,
            limit=self.TRADE_REQUEST_LIMIT,
            start_time=start_time,
            end_time=end_time,
        )

        all_trades = list(trades)

        while len(trades) == self.TRADE_REQUEST_LIMIT:
            next_from_id = trades[-1]["a"] + 1

            trades = self._get_trades_raw(
                symbol=symbol,
                limit=self.TRADE_REQUEST_LIMIT,
                from_id=next_from_id,
            )

            if not trades:
                break

            trades_in_window = [
                trade
                for trade in trades
                if start_time <= trade["T"] <= end_time
            ]

            all_trades.extend(trades_in_window)

            if len(trades_in_window) < len(trades):
                break

        return all_trades
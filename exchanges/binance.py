from urllib import response

import requests

from enums.exchange import Exchange
from exchanges.base_exchange import BaseExchange


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
    ) -> list:
        """Download raw candle data from Binance USD-M Futures."""
        normalized_symbol = self._normalize_symbol(symbol)

        response = requests.get(
        f"{self.BASE_URL}/fapi/v1/klines",
        params={
            "symbol": normalized_symbol,
            "interval": interval,
            "limit": limit,
        },
        timeout=10,
    )

        response.raise_for_status()

        return response.json()

    def _get_trades_raw(
    self,
    symbol: str,
    limit: int = 500,
    ) -> list:
        """Download raw aggregate trade data from Binance USD-M Futures."""
        normalized_symbol = self._normalize_symbol(symbol)

        response = requests.get(
            f"{self.BASE_URL}/fapi/v1/aggTrades",
            params={
                "symbol": normalized_symbol,
                "limit": limit,
            },
            timeout=10,
        )

        response.raise_for_status()

        return response.json()
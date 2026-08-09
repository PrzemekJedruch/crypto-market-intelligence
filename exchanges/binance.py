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
    
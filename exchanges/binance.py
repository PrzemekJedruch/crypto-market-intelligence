from enums.exchange import Exchange
from exchanges.base_exchange import BaseExchange


class BinanceExchange(BaseExchange):
    """Client for Binance USD-M Futures public market data API."""

    BASE_URL = "https://fapi.binance.com"

    def __init__(self):
        """Initialize the Binance exchange client."""
        super().__init__(exchange=Exchange.BINANCE)
        
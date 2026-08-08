from enums.exchange import Exchange
from exchanges.base_exchange import BaseExchange


def test_base_exchange_creation():
    """Test that BaseExchange stores the exchange identifier correctly."""
    exchange_client = BaseExchange(exchange=Exchange.BINANCE)

    assert exchange_client.exchange == Exchange.BINANCE
    
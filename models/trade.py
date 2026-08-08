from dataclasses import dataclass
from datetime import datetime

from enums.exchange import Exchange
from enums.market_type import MarketType
from enums.trade_side import TradeSide


@dataclass
class Trade:
    # Exchange from which the trade data comes
    exchange: Exchange

    # Type of market, for example spot or perpetual
    market_type: MarketType

    # Trading symbol, for example BTCUSDT
    symbol: str

    # Unique trade identifier provided by the exchange
    trade_id: int

    # Time when the trade was executed
    timestamp: datetime

    # Execution price
    price: float

    # Quantity traded
    quantity: float

    # Total trade value in quote currency, for example USDT
    quote_value: float

    # Aggressor side of the trade
    side: TradeSide
    
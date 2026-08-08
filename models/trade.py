from dataclasses import dataclass

from models.base_market_data import BaseMarketData
from enums.trade_side import TradeSide


@dataclass
class Trade(BaseMarketData):
    # Unique trade identifier provided by the exchange
    trade_id: int

    # Execution price
    price: float

    # Quantity traded
    quantity: float

    # Total trade value in quote currency, for example USDT
    quote_value: float

    # Aggressor side of the trade
    side: TradeSide

    
from enum import Enum


class TradeSide(Enum):
    # Represents an aggressive buy order
    BUY = "buy"

    # Represents an aggressive sell order
    SELL = "sell"
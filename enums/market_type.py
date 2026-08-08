from enum import Enum


class MarketType(Enum):
    # Spot market - direct purchase or sale of the asset
    SPOT = "spot"

    # Perpetual futures contract without an expiration date
    PERPETUAL = "perpetual"

    # Futures contract with a specific expiration date
    FUTURES = "futures"
    
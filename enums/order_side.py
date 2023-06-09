from enum import Enum


class OrderSide(str, Enum):
    """
    Represents what side this order was executed on.
    """

    BUY = "buy"
    SELL = "sell"

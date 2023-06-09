from enum import Enum


class OrderType(str, Enum):
    """
    Represents what type of roder this is.
    """

    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"

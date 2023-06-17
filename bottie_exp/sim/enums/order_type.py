from enum import Enum


class OrderType(Enum):
    """
    Order type
    """

    MARKET = 'market'
    LIMIT = 'limit'

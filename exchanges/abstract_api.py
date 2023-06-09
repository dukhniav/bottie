from abc import ABC, abstractmethod

from enums.order_side import OrderSide
from enums.order_type import OrderType


class ExchangeInterface(ABC):
    @abstractmethod
    def establish_connection(
        self, api_key: str, api_secret: str, training_wheels: bool
    ):
        """
        Establish exchange connection
        """
        pass

    @abstractmethod
    def get_markets(self):
        """
        Get market data
        """
        pass

    @abstractmethod
    def get_ticker(self, symbol):
        """
        Get ticker data
        """
        pass

    @abstractmethod
    def get_orderbook(self, symbol):
        """
        Get orderbook
        """
        pass

    @abstractmethod
    def buy_market_order(
        self, symbol, quantity, type=OrderType.MARKET, side=OrderSide.BUY
    ):
        """
        Place market buy order
        """
        pass

    @abstractmethod
    def buy_limit_order(
        self, symbol, quantity, price, type=OrderType.LIMIT, side=OrderSide.BUY
    ):
        """
        Place limit buy order
        """
        pass

    @abstractmethod
    def sell_market_order(
        self, symbol, quantity, type=OrderType.MARKET, side=OrderSide.SELL
    ):
        """
        Place market sell order
        """
        pass

    @abstractmethod
    def sell_limit_order(
        self, symbol, quantity, price, type=OrderType.LIMIT, side=OrderSide.SELL
    ):
        """
        Place limit sell order
        """
        pass

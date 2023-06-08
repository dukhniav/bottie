from abc import ABC, abstractmethod


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
    def create_buy_order(self, type, symbol, quantity, price, side):
        """
        Place buy order
        """
        pass

    @abstractmethod
    def create_sell_order(self, type, symbol, quantity, price, side):
        """
        Place sell order
        """
        pass

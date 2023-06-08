# Importing the API and instantiating the REST client according to our keys
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from logging import getLogger

# from utils.config import Configuration
from exchanges.abstract_api import ExchangeInterface


class AlpacaAPI(ExchangeInterface):
    def __init__(self) -> None:
        self.logger = getLogger(__name__)

        self.logger.info("Initializing Alpaca API...")

        self.api_key = None
        self.api_secret = None

    def establish_connection(
        self, api_key: str, api_secret: str, training_wheels: bool
    ):
        self.logger.info(
            f"Establishing Alpaca API connection {'with training wheels...' if training_wheels else '...'}"
        )

        trading_client = TradingClient(api_key, api_secret, paper=training_wheels)

        self.logger.info("Connection established!")
        return trading_client

    def get_markets(self):
        """
        Get market data
        """
        pass

    def get_ticker(self, symbol):
        """
        Get ticker data
        """
        pass

    def get_orderbook(self, symbol):
        """
        Get orderbook
        """
        pass

    def create_buy_order(self, type, symbol, quantity, price, side):
        """
        Create buy order
        """
        self.market_order_data = MarketOrderRequest(
            symbol="BTC/USD", qty=1, side=OrderSide.BUY, time_in_force=TimeInForce.GTC
        )

    def create_sell_order(self, type, symbol, quantity, price, side):
        """
        Create sell order
        """
        pass

    def get_account(self, trading_client: TradingClient):
        # Getting account information and printing it
        self.logger.info("Getting alpaca account info...")

        account = trading_client.get_account()

        for property_name, value in account:
            print(f'"{property_name}": {value}')

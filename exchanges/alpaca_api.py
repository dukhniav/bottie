# Importing the API and instantiating the REST client according to our keys
from alpaca.trading.client import TradingClient

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
        trading_client = TradingClient(api_key, api_secret, paper=training_wheels)

        return trading_client

    def get_account(self):
        # Getting account information and printing it
        account = self.trading_client.get_account()

        for property_name, value in account:
            print(f'"{property_name}": {value}')

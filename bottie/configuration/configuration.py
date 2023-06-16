import json
import logging

from typing import Any, List


from bottie import constants

logger = logging.getLogger()


class Configuration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        logger.info("Initializing config...")
        self._load_config()
        # Add more configuration attributes as needed

    def _load_config(self):
        logger.info("Loading config files...")
        with open(constants.CONFIG_FILE_PATH) as file:
            self._config = json.load(file)
        file.close()

        with open(constants.CREDENTIALS_FILE_PATH) as file:
            self._credentials = json.load(file)
        file.close()

    # Function to write data to the JSON file
    def _update_config(self):
        logger.info("Updating config file...")

        with open(constants.CONFIG_FILE_PATH, 'w') as file:
            json.dump(self._config, file)
        file.close()

    # Config
    def reload_config(self):
        """
        Reload configuration files.
        """
        logger.info("Reloading config...")

        self._load_config()

    # Function to create a new ticker

    def add_ticker(self, ticker: str):
        logger.info(f"Adding ticker: {ticker}.")

        tickers: List = self.get_tickers()
        tickers.append(ticker)
        self._update_config()

    def get_tickers(self):
        logger.info("Retrieving tickers from config.")

        # Function to read all tickers
        tickers = self._config['tickers']
        return tickers

    def update_ticker(self, old_ticker, new_ticker):
        logger.info(f"Updating ticker: {old_ticker} -> {new_ticker}")

        # Function to update a ticker
        tickers: List = self.get_tickers()
        if old_ticker in tickers:
            index = tickers.index(old_ticker)
            tickers[index] = new_ticker
            self._update_config()

    def delete_ticker(self, ticker: str):
        logger.info(f"Deleting ticker: {ticker}")

        # Function to delete a ticker
        tickers: List = self.get_tickers()
        if ticker in tickers:
            tickers.remove(ticker)
            self._update_config()

    # Dry run config
    def get_starting_funds(self):
        return self._config["paper_starting_balance"]

    # Operation config
    def get_market_data_source(self):
        return constants.MARKET_DATA

    def is_paper_trading(self):
        return self._config["paper_trading"]

    def get_db_url(self):
        return self._config["db_url"]

    def get_initial_state(self):
        return self._config['initial_state']

    def get_default_timeframe(self):
        return self._config['timeframe']

    # API config

    def get_finnhub_credentials(self) -> list:
        _finnhub = self._credentials['finnhub']
        return {'api_key': _finnhub['api_key'], 'webhook_secret': _finnhub['webhook_secret']}


# def setup_logging_config(self):
#     self.
config = Configuration()

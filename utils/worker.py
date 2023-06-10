import time

from datetime import datetime
from logging import getLogger

from utils.utils import Utils
from utils.config import Configuration
from interfaces.finnhub_api import Finnhub
from utils.transactions import Transaction


class Worker:
    def __init__(self, utils: Utils, config: Configuration):
        self.logger = getLogger(__name__)
        self.logger.info("Initializing worker...")

        self.running = False
        self.utils = utils
        self.config = config

        # Initialize market data
        self.md = Finnhub(self.config.FINNHUB_API_KEY)

    def start(self):
        self.logger.info("Starting worker...")

        self.running = True

        self.logger.info("Worker started!")

        self.process()

    def stop(self):
        self.logger.info("Stopping worker...")

        self.running = False

    def is_running(self):
        return self.running

    def process(self):
        while self.running:
            # Worker continues its processing

            # Get market data
            # Analyze data
            # Generate signals
            # Execute trades

            self.utils.start_heartbeat()
            time.sleep(1)

    def get_ticker_candles(self, ticker, tf, data_from, data_to=datetime.now()):
        data_from = int(self.utils.convert_timestamp(data_from))
        data_to = int(self.utils.convert_timestamp(data_to))
        return self.md.retrieve_stock_data(ticker, tf, data_from, data_to)

    def get_ticker_quote(self, ticker):
        return self.md.get_quote(ticker)

from logging import getLogger

from utils.config import Configuration


class TickerManager:
    def __init__(self, config: Configuration):
        self.logger = getLogger(__name__)
        self.logger.info("Initializing ticker manager...")

        self.config = config

    def add_ticker(self, ticker) -> bool:
        status = self.config.add_ticker(ticker)
        return status

    def remove_ticker(self, ticker):
        status = self.config.remove_ticker(ticker)
        if not status:
            print(f"Failed to remove {ticker}.")

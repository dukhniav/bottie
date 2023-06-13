import logging
import threading
import time

from typing import Any, Dict

from bottie import __version__

from bottie.apis.finnhub_api import Finnhub

from bottie.managers.account_manager import AccountManager
from bottie.managers.transaction_manager import TransactionManager

from bottie.enums.order_side import OrderSide
from bottie.enums.state import State
from bottie.enums.order_type import OrderType


from bottie.configuration.configuration import config

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, finnhub_api: Finnhub, account_manager: AccountManager, transactions_manager: TransactionManager) -> None:
        logger.info(f"Initializing worker (ver={__version__})")
        self._stop_event = threading.Event()
        self._worker_thread = None
        self.account = account_manager.get_account_by_name()
        self.transactions = transactions_manager
        self.finnhub = finnhub_api  # Variable to hold the market data source
        self.tickers = config.get_tickers()
        self._state = State.STOPPED

    # def start(self) -> bool:
    #     logger.info("Starting worker...")
    #     self._stop_event.clear()
    #     self._worker_thread = threading.Thread(target=self._worker_loop)
    #     self._worker_thread.start()
    #     return True

    def start(self) -> bool:
        logger.info("Starting worker...")
        self._state = State.RUNNING
        self._worker_loop()
        return True

    # def stop(self) -> bool:
    #     logger.info("Stopping worker...")
    #     self._stop_event.set()
    #     self._worker_thread.join()  # Wait for the worker thread to finish
    #     self._worker_thread = None  # Reset the worker thread variable
    #     return True

    def stop(self) -> bool:
        logger.info("Stopping worker...")
        self._state = State.STOPPED

        return True

    def market_data_source(self, source):
        self.md = source

    def _worker_loop(self):
        while self._state == State.RUNNING:
            # Retrieve market data from the data source (Finnhub API)
            for ticker in self.tickers:
                market_data = self.get_market_data(ticker)

                if market_data:
                    # Perform analysis on market data
                    signal = self.analyze_market_data(market_data)

                    # Generate orders based on the signals
                    orders = self.generate_orders(signal)

                    # Execute the generated orders
                    self.execute_orders(orders)
                else:
                    logger.debug("Unable to retrieve market data")

            time.sleep(10)  # Sleep for some time before the next iteration

        logger.info("Worker stopped.")

    def get_market_data(self, ticker: str):
        md = self.finnhub.get_quote(ticker)
        logger.info(f"Retrieving market data for ticker: {ticker}")

        return md

    def analyze_market_data(self, market_data) -> Dict:
        logger.debug(
            f"Analying market data for ticker: {market_data['ticker']}")
        # Perform analysis on the market data
        # Implement your own analysis logic here
        # Example: Generate a random signal for demonstration purposes
        if market_data:
            signal = {
                'ticker': market_data['ticker'],
                'signal_type': OrderSide.BUY,
                'price': market_data['price'],
                'timestamp': market_data['timestamp']
            }

        return signal

    def generate_orders(self, signal: Dict) -> Dict:
        # Generate orders based on the signals
        # Implement your own order generation logic here

        # Example: Generate a market buy order for each signal
        if signal:
            order = {
                'ticker': signal['ticker'],
                'order_type': OrderType.MARKET,
                'action': OrderSide.BUY,
                'quantity': 1,
                'price': 0
            }

        return order

    def execute_orders(self, order):
        # Execute the generated orders
        # Implement your own order execution logic here
        if order:
            # Example: Print the order details
            ticker = order['ticker']
            _type: OrderType = order['order_type']
            side: OrderSide = order['action']
            quantity = order['quantity']
            price = 0 if _type == OrderType.MARKET else order['price']

            logger.info(
                f"Executing {_type}-{side} order for {quantity} of {ticker}")
            # Execute the order using the appropriate API or method
            # Logging the execution status
            status = ''

            status = self.transactions.create_transaction(
                ticker, quantity, price)
            if status == 'TransactionType.PENDING':
                status = self.transactions.process_transactions()

                if status == 'TransactionType.PROCESSED':
                    logger.info(f"Order executed successfully: {order}")
                else:
                    logger.info(f"Transaction failed to process.")
            else:
                logger.debug("Failed to create transaction")

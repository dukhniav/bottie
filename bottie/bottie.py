import logging
import threading
import time

from typing import Dict

from bottie import __version__
from bottie.managers.account_manager import AccountManager
from bottie.managers.transaction_manager import TransactionManager
from bottie.helpers.db_helper import initialize_models
from bottie.utils.gc_setup import gc_set_threshold
from bottie.worker import Worker
from bottie.configuration.configuration import config
from bottie.apis.finnhub_api import Finnhub
from bottie.enums.menu_options import MenuOptions

logger = logging.getLogger(__name__)


class Bottie:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Bottie, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        logger.info("Initializing Bottie...")

        # Setup
        self._setup()
        self.account = AccountManager()
        self.transactions = TransactionManager()

        self.finnhub_api = Finnhub()

        # Create worker instance
        self.worker = Worker(self.finnhub_api, self.account, self.transactions)

        # Create a lock for worker thread synchronization
        self.worker_lock = threading.Lock()

        # Create a reference to the worker thread
        self.worker_thread = None

    def _setup(self):
        initialize_models()

    def start_worker(self):
        logger.info("Starting worker...")
        with self.worker_lock:
            if not self.worker_thread or not self.worker_thread.is_alive():
                # Create and start the worker thread
                self.worker_thread = threading.Thread(target=self.worker.start)
                self.worker_thread.start()
                return True
        return False

    def stop_worker(self):
        logger.info("Stopping worker...")
        with self.worker_lock:
            if self.worker_thread and self.worker_thread.is_alive():
                self.worker.stop()
                self.worker_thread.join()
                self.worker_thread = None
                return True
        return False

    def show_available_funds(self):
        return self.account.get_account_available_funds()

    def get_quote(self) -> Dict:
        ticker = input("Ticker for quote: ")
        quote: Dict = {'ticker': ticker,
                       'quote': self.finnhub_api.get_quote(ticker)}
        return quote

    def reload_config(self) -> bool:
        status = True
        try:
            config.reload_config()
        except:
            status = False

        return status

    def restart_bot(self):
        # Stop the worker thread
        self.stop_worker()

        # Optionally perform any additional cleanup or shutdown tasks here

        # Wait for a brief moment to ensure the worker is fully stopped
        time.sleep(1)

        # Perform any necessary setup before starting the bot again
        self._setup()

        logger.info(f"bottie {__version__}")
        gc_set_threshold()

        # Start the worker thread again
        self.start_worker()

        logger.info("Bot restarted.")


bottie = Bottie()

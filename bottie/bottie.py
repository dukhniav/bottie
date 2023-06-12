import logging
import threading
import time

from typing import Dict

from bottie import __version__

from bottie.managers.account_manager import AccountManager
from bottie.helpers.db_helper import initialize_models

from bottie.utils.gc_setup import gc_set_threshold


from bottie.worker import Worker

from bottie.configuration.configuration import config
from bottie import constants

from bottie.apis.finnhub_api import Finnhub

# from bottie.utils.menu import run_menu_in_thread
from bottie.enums.menu_options import MenuOptions

logger = logging.getLogger(__name__)


class Bottie:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Bottie, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        logger.info("Initializing Bottie...")

        # Setup
        self._setup()
        self.account = AccountManager()

        self.finnhub_api = Finnhub()

        # Start worker
        self.worker = Worker()

    def _setup(self):
        initialize_models()

    # Main menu manager
    def start_worker(self):
        return self.worker.start()

    def stop_worker(self):
        logger.info("Stopping worker...")
        return self.worker.stop() if self.worker else False

    def show_available_funds(self):
        return self.account.get_account_available_funds()

    def get_quote(self) -> Dict:
        ticker = input("Ticker for quote: ")
        quote: Dict = {'ticker': ticker,
                       'quote': self.finnhub_api.get_quote(ticker)}
        return quote

    def reload_config() -> bool:
        status = True
        try:
            config.reload_config()
        except:
            status = False

        return status

    def restart_bot(self):
        # Stop the worker thread
        stop_worker_thread = threading.Thread(target=self.stop_worker)
        stop_worker_thread.start()
        stop_worker_thread.join()

        # Optionally perform any additional cleanup or shutdown tasks here

        # Wait for a brief moment to ensure the worker is fully stopped
        time.sleep(1)

        # Perform any necessary setup before starting the bot again
        self._setup()

        logger.info(f"bottie {__version__}")
        gc_set_threshold()

        # Start the worker thread again
        start_worker_thread = threading.Thread(target=self.start_worker)
        start_worker_thread.start()

        logger.info("Bot restarted.")


bottie = Bottie()

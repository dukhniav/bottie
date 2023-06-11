import logging

from typing import Dict

from bottie.managers.account_manager import AccountManager
from bottie.helpers.db_helper import initialize_models

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
        return self.worker.stop()

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


bottie = Bottie()

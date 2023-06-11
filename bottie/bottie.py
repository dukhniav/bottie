import logging

from bottie.managers.account_manager import AccountManager
from bottie.helpers.db_helper import initialize_models

from bottie.worker import Worker

from bottie.configuration.configuration import config
from bottie import constants

from bottie.utils.menu import run_menu_in_thread
from bottie.enums.menu_options import MenuOptions

logger = logging.getLogger(__name__)


class Bottie:
    def __init__(self) -> None:
        logger.info("Initializing Bottie...")

        # Setup
        self._setup()
        self.account = AccountManager()

        # Start worker
        self.worker = Worker()

    def _setup(self):
        initialize_models()

    def run(self):
        run_menu_in_thread(self.handle_menu_action)

    def handle_menu_action(self, result):
        match result:
            case MenuOptions.START:
                self.start_worker()
            case MenuOptions.STOP:
                self.stop_worker()
            case MenuOptions.ACCOUNT_BALANCE:
                self.account.get_total_funds()
            case MenuOptions.ACCOUNT_AVAILABLE:
                self.account.get_account_available_funds(
                    self.account.get_account_by_name())
            case MenuOptions.CONFIG_RELOAD:
                pass
            case MenuOptions.CONFIG_ADD_TICKER:
                pass
            case MenuOptions.CONFIG_VIEW_TICKERS:
                pass
            case MenuOptions.CONFIG_REMOVE_TICKER:
                pass
            case MenuOptions.MANUAL_QUOTE:
                pass
            case MenuOptions.MANUAL_TRADE:
                pass
            case MenuOptions.MANUAL_PENDING:
                pass
            case MenuOptions.MANUAL_GET_TRADES:
                pass

    def start_worker(self):
        self.worker.start()

    def stop_worker(self):
        pass

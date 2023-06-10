import logging

from bottie.managers.account_manager import AccountManager
from bottie.helpers.db_helper import initialize_models

from bottie.configuration.configuration import config
from bottie import constants

logger = logging.getLogger(__name__)


class Bottie:
    def __init__(self) -> None:
        logger.info("Initializing Bottie...")

        # Setup
        self._setup()
        self.account = AccountManager()

        print(self.account.get_accounts())

    def _setup(self):
        initialize_models()

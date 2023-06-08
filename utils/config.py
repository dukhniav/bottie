import json

from logging import getLogger

from enums.exchange import Exchange


CONFIG_FILE_PATH = "config/config.json"
CREDENTIALS_FILE_PATH = "config/credentials.json"


class Configuration:
    def __init__(self):
        self.logger = getLogger(__name__)

        self.logger.info("Initialing config...")

        with open(CONFIG_FILE_PATH) as file:
            self._config = json.load(file)
        file.close()

        with open(CREDENTIALS_FILE_PATH) as file:
            self._credentials = json.load(file)
        file.close()

        self.CURRENCY = self._config["currency"]

        self.HEARTBEAT_FREQUENCY = self._config["heartbeat_frequency"]

        self.TRAINING_WHEELS = self._config["training_wheels"]

        # Live exchange
        try:
            exchange_live = (
                self._config["exchange"] if self._config["exchange"] != "" else None
            )
        except:
            exchange_live = None

        # Paper exchange
        try:
            exchange_paper = (
                self._config["paper_exchange"]
                if self._config["paper_exchange"] != ""
                else None
            )
        except:
            exchange_paper = None

        self.EXCHANGE = self.get_trading_exchange(exchange_live, exchange_paper)

    def get_exchange_credentials(self, exchange: Exchange):
        self.logger.info("Getting exchange credentials")
        if exchange == Exchange.ALPACA.name:
            alpaca_credentials = self._credentials["alpaca"]
            self.EXCHANGE_API_KEY = alpaca_credentials["client_id"]
            self.EXCHANGE_API_SECRET = alpaca_credentials["client_secret"]
        else:
            self.logger.debug(
                f"No exchange specified, or something went wrong. {exchange}"
            )

    def get_trading_exchange(self, live_exchange, paper_exchange):
        # TODO: add edge cases / validate
        # TODO: add default live trading exchange

        if self.TRAINING_WHEELS:
            # Paper trading
            if paper_exchange:
                return paper_exchange
            else:
                return Exchange.ALPACA
        else:
            # Live trading
            if live_exchange:
                return live_exchange
            else:
                return ""

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

        # Finnhub credentials
        finnhub = self._credentials["finnhub"]
        self.FINNHUB_API_KEY = finnhub["api_key"]
        self.FINNHUB_WEB_SECRET = finnhub["webhook_secret"]

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

    def get_tickers(self) -> list:
        return self._config["tickers"]

    def save_tickers(self):
        with open(CONFIG_FILE_PATH, "w") as file:
            json.dump(self._config, file, indent=4)

    def add_ticker(self, ticker: str) -> bool:
        try:
            tickers = self.get_tickers()
            tickers.append(ticker)

            self._config["tickers"] = tickers
            self.save_tickers()

            self.logger.info(f"Added {ticker} to tickers.")

            return True
        except Exception as e:
            self.logger.debug(f"Failed adding new ticker. Error: {e}")
            return False

    def remove_ticker(self, ticker: str) -> bool:
        try:
            tickers = self.get_tickers()

            if ticker in tickers:
                tickers.remove(ticker)

                self.save_tickers()

                self.logger.info(f"Removed {ticker} from tickers.")

                return True
            else:
                print("Ticker not found.")

                return False

        except Exception as e:
            self.logger.debug(f"Failed to remove {ticker} with error: {e}")

            return False

    def view_config(self):
        print("Configuration:")
        print(f"Tickers: {', '.join(self._config['tickers'])}")
        print(f"Strategy: {self._config['strategy']}")
        print(f"Currency: {self._config['currency']}")
        print(f"Sentiment Enabled: {self._config['sentiment']['enabled']}")
        print(f"Positive Range: {self._config['sentiment']['positive_range']}")
        print(f"Sentiment Sources: {', '.join(self._config['sentiment']['sources'])}")
        print(f"Heartbeat Frequency: {self._config['heartbeat_frequency']}")
        print(f"Training Wheels: {self._config['training_wheels']}")
        print(f"Ticker Update Interval: {self._config['ticker_update_interval']}")
        print(f"Exchange: {self._config['exchange']}")
        print(f"Paper Exchange: {self._config['paper_exchange']}")

import finnhub
import logging
import datetime
import json

from typing import Dict
from os import path

from datetime import datetime

logger = logging.getLogger(__name__)

CREDENTIALS_FILE_PATH = 'credentials.json'


class Finnhub:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Finnhub, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        logger.info("Starting Finnhub API manager...")
        _api_key = self.load_api_key()
        # Setup client
        self.client = finnhub.Client(api_key=_api_key)

    @staticmethod
    def load_api_key():
        with open(CREDENTIALS_FILE_PATH) as file:
            data = json.load(file)
        file.close()

        api_key = data['finnhub']

        return api_key

    def get_historical_data(self, symbol, start_date, end_date):
        data = None
        data = self.client.stock_candles(
            symbol=symbol, resolution=config.get_default_timeframe, _from=start_date, to=end_date)
        return data

    def get_quote(self, ticker: str):
        """Get current ticker price

        Args:
            ticker (str): ticker symbol

        Returns:
            _type_: price
        """

        temp_quote = self.client.quote(symbol=ticker)
        quote: Dict = {
            "ticker": ticker,
            "price": temp_quote.get("c"),
            "delta": temp_quote.get("d"),
            "delta_percent": temp_quote.get("dp"),
            "high": temp_quote.get("h"),
            "low": temp_quote.get("l"),
            "open": temp_quote.get("o"),
            "close_prev": temp_quote.get("pc"),
            "timestamp": datetime.now()
        }

        return quote

    def retrieve_stock_data(
        self, ticker: str, timeframe: str, data_from: str, data_to: str
    ):
        """Get candlestick data (OHLCV) for stocks.
        Daily data will be adjusted for Splits. Intraday data will remain unadjusted.

        Args:
            ticker (str): ticker symbol
            timeframe (str): timeframe resolution - Supported timeframes 1, 5, 15, 30, 60, D, W, M.
                  Some timeframes might not be available depending on the exchange.
            data_from (str): UNIX timestamp. Interval initial value.
            data_to (str): UNIX timestamp. Interval end value.
        """
        temp_data = self.client.stock_candles(
            symbol=ticker, resolution=timeframe, _from=data_from, to=data_to
        )
        data = {
            "close": temp_data.get("c"),
            "high": temp_data.get("h"),
            "low": temp_data.get("l"),
            "open": temp_data.get("o"),
            "status": temp_data.get("s"),
            "time_stamp": temp_data.get("t"),
            "volume": temp_data.get("v"),
        }
        return data


finnhub_api = Finnhub()

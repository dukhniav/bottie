import finnhub

from datetime import datetime


class Finnhub:
    def __init__(self, api_key: str) -> None:
        # Setup client
        self.client = finnhub.Client(api_key=api_key)

    def get_quote(self, ticker: str):
        """Get current ticker price

        Args:
            ticker (str): ticker symbol

        Returns:
            _type_: price
        """

        temp_quote = self.client.quote(symbol=ticker)
        quote = {
            "price": temp_quote.get("c"),
            "delta": temp_quote.get("d"),
            "delta_percent": temp_quote.get("dp"),
            "high": temp_quote.get("h"),
            "low": temp_quote.get("l"),
            "open": temp_quote.get("o"),
            "close_prev": temp_quote.get("pc"),
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

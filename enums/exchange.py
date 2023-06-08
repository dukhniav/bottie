from enum import Enum

from exchanges.alpaca_api import AlpacaAPI as Alpaca


class Exchange(Enum):
    BINANCE = "binance"
    COINBASE = "coinbase"
    KRAKEN = "kraken"
    MARKETWATCH = "marketwatch"
    INVESTOPEDIA = "investopedia"
    FINVIZ = "finviz"
    THINKORSWIM = "thinkorswim"
    ETORO = "etoro"
    ALPACA = "alpaca"

    def create_api(self):
        if self == Exchange.BINANCE:
            return BinanceAPI()
        elif self == Exchange.COINBASE:
            return CoinbaseAPI()
        elif self == Exchange.KRAKEN:
            return KrakenAPI()
        elif self == Exchange.MARKETWATCH:
            return KrakenAPI()
        elif self == Exchange.INVESTOPEDIA:
            return KrakenAPI()
        elif self == Exchange.FINVIZ:
            return KrakenAPI()
        elif self == Exchange.THINKORSWIM:
            return KrakenAPI()
        elif self == Exchange.ETORO:
            return etoro()
        elif self == Exchange.ALPACA:
            return AlpacaAPI()
        else:
            raise ValueError("Invalid exchange")


class BinanceAPI:
    def __init__(self):
        # Initialization code for Binance API
        pass


class CoinbaseAPI:
    def __init__(self):
        # Initialization code for Coinbase API
        pass


class KrakenAPI:
    def __init__(self):
        # Initialization code for Kraken API
        pass


class MarketwatchAPI:
    def __init__(self):
        # Initialization code for Marketwatch API
        pass


class InvestopediaAPI:
    def __init__(self):
        # Initialization code for Investopedia API
        pass


class FinvizAPI:
    def __init__(self):
        # Initialization code for Finviz API
        pass


class ThinkOrSwimAPI:
    def __init__(self):
        # Initialization code for ThinkOrSwim API
        pass


class eToroAPI:
    def __init__(self):
        # Initialization code for eToro API
        pass


class AlpacaAPI:
    def __init__(self):
        # Initialization code for eToro API
        self.exchange = Alpaca()

# Importing the API and instantiating the REST client according to our keys
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import alpaca_trade_api as tradeapi


from logging import getLogger

# from utils.config import Configuration
from exchanges.abstract_api import ExchangeInterface
from enums.order_type import OrderType


class AlpacaAPI(ExchangeInterface):
    def __init__(self) -> None:
        self.logger = getLogger(__name__)

        self.logger.info("Initializing Alpaca API...")

        self.api_key = None
        self.api_secret = None

    def establish_connection(
        self, api_key: str, api_secret: str, training_wheels: bool
    ):
        self.logger.info(
            f"Establishing Alpaca API connection {'with training wheels...' if training_wheels else '...'}"
        )

        trading_client = TradingClient(api_key, api_secret, paper=training_wheels)

        self.logger.info("Connection established!")
        return trading_client

    def get_open_positions(self, trading_client: TradingClient):
        # Get all open positions and print each of them
        positions = trading_client.get_all_positions()
        for position in positions:
            for property_name, value in position:
                print(f'"{property_name}": {value}')

    def get_markets(self):
        """
        Get market data
        """
        pass

    def get_ticker(self, symbol):
        """
        Get ticker data
        """
        pass

    def get_orderbook(self, symbol):
        """
        Get orderbook
        """
        pass

    def get_account(self, trading_client: TradingClient):
        # Getting account information and printing it
        self.logger.info("Getting alpaca account info...")

        # Get our account information.
        account = trading_client.get_account()

        # Check if our account is restricted from trading.
        if account.trading_blocked:
            print("Account is currently restricted from trading.")
        else:
            # Check how much money we can use to open new positions.
            print("${} is available as buying power.".format(account.buying_power))

    def get_portfolio_delta(self, trading_client: TradingClient):
        # Get our account information.
        account = trading_client.get_account()

        # Check our current balance vs. our balance at the last market close
        balance_change = float(account.equity) - float(account.last_equity)
        print(f"Today's portfolio balance change: ${balance_change}")

    def market_order(
        self,
        tc: TradingClient,
        symbol: str,
        quantity: float,
        side: OrderSide,
    ):
        """
        Place market buy order
        """
        # preparing market order
        market_order_data = MarketOrderRequest(
            symbol=symbol, qty=quantity, side=side, time_in_force=TimeInForce.DAY
        )

        # Market order
        market_order = tc.submit_order(order_data=market_order_data)

    def limit_order(
        self,
        tc: TradingClient,
        symbol: str,
        quantity: float,
        price: float,
        side: OrderSide,
    ):
        """
        Place limit buy order
        """
        # preparing limit order
        limit_order_data = LimitOrderRequest(
            symbol=symbol,
            quantity=quantity,
            limit_price=price,
            notional=4000,
            side=side,
            time_in_force=TimeInForce.FOK,
        )

        # Limit order
        limit_order = tc.submit_order(order_data=limit_order_data)

    def stop_order(
        self,
        tc: TradingClient,
        symbol: str,
        quantity: float,
        side: OrderSide,
        type: OrderType = OrderType.STOP,
    ):
        """
        Place stop buy order
        """
        pass

    def stop_limit_order(
        self,
        tc: TradingClient,
        symbol: str,
        quantity: float,
        side: OrderSide,
        type: OrderType = OrderType.STOP_LIMIT,
    ):
        """
        Place stop limit buy order
        """
        pass

    def trailing_stop_order(
        self,
        tc: TradingClient,
        symbol: str,
        quantity: float,
        trail_price: float,
        side: OrderSide,
        type=OrderType.TRAILING_STOP,
    ):
        """
        Place trailing stop buy order
        """

        api = tradeapi.REST()

        # Submit a market order to buy 1 share of Apple at market price
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side=side,
            type=OrderType.MARKET,
            time_in_force="gtc",
        )

        # Submit a trailing stop order to sell 1 share of Apple at a
        # trailing stop of
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side=side,
            type=type,
            trail_price=trail_price,  # stop price will be hwm - 1.00$
            time_in_force="gtc",
        )

        # Alternatively, you could use trail_percent:
        api.submit_order(
            symbol="AAPL",
            qty=1,
            side="sell",
            type="trailing_stop",
            trail_percent=1.0,  # stop price will be hwm*0.99
            time_in_force="gtc",
        )

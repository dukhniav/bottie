from abc import ABC, abstractmethod

from enums.order_side import OrderSide
from enums.order_type import OrderType


class ExchangeInterface(ABC):
    @abstractmethod
    def establish_connection(
        self, api_key: str, api_secret: str, training_wheels: bool
    ):
        """
        Establish exchange connection
        """
        pass

    @abstractmethod
    def get_markets(self):
        """
        Get market data
        """
        pass

    @abstractmethod
    def get_ticker(self, symbol):
        """
        Get ticker data
        """
        pass

    @abstractmethod
    def get_orderbook(self, symbol):
        """
        Get orderbook
        """
        pass

    @abstractmethod
    def market_order(self, symbol: str, quantity: float, side: OrderSide):
        """
        Place market buy order.

        A market order is a request to buy or sell a security at the currently available market price. It provides the
        most likely method of filling an order. Market orders fill nearly instantaneously.

        As a trade-off, your fill price may slip depending on the available liquidity at each price level as well as any
        price moves that may occur while your order is being routed to its execution venue. There is also the risk with
        market orders that they may get filled at unexpected prices due to short-term price spikes.
        """
        pass

    @abstractmethod
    def limit_order(self, symbol: str, quantity: float, price: float, side: OrderSide):
        """
        Place limit buy order.

        A limit order is an order to buy or sell at a specified price or better. A buy limit order (a limit order to buy)
        is executed at the specified limit price or lower (i.e., better). Conversely, a sell limit order (a limit order to
        sell) is executed at the specified limit price or higher (better). Unlike a market order, you have to specify the
        limit price parameter when submitting your order.

        While a limit order can prevent slippage, it may not be filled for a quite a bit of time, if at all. For a buy limit
        order, if the market price is within your specified limit price, you can expect the order to be filled. If the market
        price is equivalent to your limit price, your order may or may not be filled; if the order cannot immediately execute
        against resting liquidity, then it is deemed non-marketable and will only be filled once a marketable order interacts
        with it. You could miss a trading opportunity if price moves away from the limit price before your order can be filled.
        """
        pass

    @abstractmethod
    def stop_order(self, symbol: str, quantity: float, side: OrderSide):
        """
        Place stop buy order.

        A stop (market) order is an order to buy or sell a security when its price moves past a particular point, ensuring
        a higher probability of achieving a predetermined entry or exit price. Once the order is elected, the stop order
        becomes a market order. Alpaca converts buy stop orders into stop limit orders with a limit price that is 4% higher
        than a stop price < $50 (or 2.5% higher than a stop price >= $50). Sell stop orders are not converted into stop limit orders.

        A stop order does not guarantee the order will be filled at a certain price after it is converted to a market order.
        """
        pass

    @abstractmethod
    def stop_limit_order(self, symbol: str, quantity: float, side: OrderSide):
        """
        Place stop limit buy order.

        A stop-limit order is a conditional trade over a set time frame that combines the features of a stop order with
        those of a limit order and is used to mitigate risk. The stop-limit order will be executed at a specified limit
        price, or better, after a given stop price has been reached. Once the stop price is reached, the stop-limit order
        becomes a limit order to buy or sell at the limit price or better. In the case of a gap down in the market that
        causes the election of your order, but not the execution, you order will remain active as a limit order until it
        is executable or cancelled.

        In order to submit a stop limit order, you will need to specify both the limit and stop price parameters in the API.
        """
        pass

    @abstractmethod
    def trailing_stop_order(
        self, symbol: str, trail_price: float, quantity: float, side: OrderSide
    ):
        """
        Place trailing stop buy order.

        Trailing stop orders allow you to continuously and automatically keep updating the stop price threshold based
        on the stock price movement. You request a single order with a dollar offset value or percentage value as the trail
        and the actual stop price for this order changes as the stock price moves in your favorable way, or stay at the
        last level otherwise. This way, you don’t need to monitor the price movement and keep sending replace requests to
        update the stop price close to the latest market movement.

        Trailing stop orders keep track of the highest (for sell, lowest for buy) prices (called high water mark, or hwm)
        since the order was submitted, and the user-specified trail parameters determine the actual stop price to trigger
        relative to high water mark. Once the stop price is triggered, the order turns into a market order, and it may
        fill above or below the stop trigger price.
        """
        pass

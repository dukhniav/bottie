from logging import getLogger

from interfaces.finnhub_api import Finnhub
from utils.db import DB


class Account:
    def __init__(self, finnhub: Finnhub, db: DB):
        self.logger = getLogger(__name__)
        self.logger.info("Initializing account...")

        self.finnhub = finnhub
        self.db = db

        # Initialize portfolio
        self.trades = []
        self.portfolio = {}

    # Funds
    # Portfolio

    def get_available_funds(self):
        pass

    def get_pending_trades(self):
        pass

    def reset_portfolio(self):
        pass

    def _trade(self, symbol, quantity, price):
        # Simulate placing a trade
        trade = {"symbol": symbol, "quantity": quantity, "price": price}
        self.trades.append(trade)
        print(f"Trade placed: {symbol} - Quantity: {quantity} - Price: {price}")

    def update_portfolio(self, symbol, quantity):
        # Update the portfolio holdings for a given symbol
        self.portfolio[symbol] = quantity
        print(f"Portfolio updated: {symbol} - Quantity: {quantity}")

    def get_portfolio(self):
        # Retrieve the current portfolio holdings
        return self.portfolio

    def calculate_portfolio_value(self):
        # Calculate the current value of the portfolio based on provided prices
        total_value = 0
        for symbol, quantity in self.portfolio.items():
            price = self.finnhub.get_quote(symbol)["price"]
            value = price * quantity
            total_value += value
        print("=================================")
        print(f"Portfolio worth: ${total_value}")

    def create_account():
        pass

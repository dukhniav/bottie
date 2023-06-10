import threading

from logging import getLogger

from account import Account
from utils.worker import Worker
from utils.config import Configuration
from utils.utils import Utils
from utils.ticker_manager import TickerManager
from utils.db import DB
from utils.menu import Menu


class Bottie:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.logger.info("Initializing Bottie...")

        self.setup()
        self.setup_menu()

        self.worker_thread = None

    def setup(self):
        self.logger.info("Initializing modules...")
        self.config = Configuration()
        self.utils = Utils(self.config)
        self.ticker_manager = TickerManager(self.config)
        self.worker = Worker(self.utils, self.config)
        self.account = Account(self.worker.md)
        self.db = DB(self.config.DB_NAME)

    def setup_menu(self):
        self.menu = Menu()

        # Initialize the main menu options
        self.menu.add_option(1, "Start Bot", self.start_bot)
        self.menu.add_option(2, "Stop Bot", self.stop_bot)
        self.menu.add_option(3, "View Config", self.view_config)

        # Initialize the ticker management submenu options
        ticker_menu = Menu()
        ticker_menu.add_option(1, "Add Ticker", self.add_ticker)
        ticker_menu.add_option(2, "Remove Ticker", self.remove_ticker)
        ticker_menu.add_option(3, "Back to Main Menu", None)
        self.menu.add_option(4, "Ticker Management", ticker_menu.display_menu)

        # Initialize the account management submenu options
        account_menu = Menu()
        # account_menu.add_option(1, "Create Account", self.account.create_account)
        account_menu.add_option(
            1, "Get Account Worth", self.account.calculate_portfolio_value
        )
        account_menu.add_option(2, "Get Portfolio", self.account.get_portfolio)
        account_menu.add_option(3, "Reset Portfolio", self.account.reset_portfolio)
        account_menu.add_option(4, "Back to Main Menu", None)
        self.menu.add_option(5, "Account Management", account_menu.display_menu)

        self.menu.add_option(6, "Exit", None)

    def run(self):
        self.logger.info("Starting Bottie...")

        self.menu.display_menu()

    def testing_functionality(self):
        _from = "6/1/23"
        to = "6/2/23"
        ticker = "aapl"

        tf = self.worker.get_ticker_candles("aapl", "60", _from, to)
        print(tf)
        print("----------------------=========================")
        print(self.utils.convert_to_dataframe(tf))

        print("----------------------=========================")
        curr_price = self.worker.get_ticker_quote(ticker)
        print(curr_price)
        print("----------------------=========================")

        print(curr_price.get("high"))

    def test_historical(self):
        pass

    def start_bot(self):
        if not self.worker_thread or not self.worker_thread.is_alive():
            self.worker_thread = threading.Thread(target=self.worker.start)
            self.worker_thread.start()
            print("Bot started.")
        else:
            print("Bot is already running.")

    def stop_bot(self):
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker.stop()
            self.worker_thread.join()
            print("Bot stopped.")
        else:
            print("Bot is not currently running.")

    def view_config(self):
        self.config.view_config()

    def view_tickers(self):
        tickers = self.config.get_tickers()
        print(tickers)

    def add_ticker(self):
        ticker = input("Enter the ticker to add: ")
        self.ticker_manager.add_ticker(ticker)
        print(f"Ticker '{ticker}' added successfully.")

    def remove_ticker(self):
        ticker = input("Enter the ticker to remove: ")
        self.ticker_manager.remove_ticker(ticker)
        print(f"Ticker '{ticker}' removed successfully.")


if __name__ == "__main__":
    bot = Bottie()
    bot.run()

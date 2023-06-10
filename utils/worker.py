import time

from logging import getLogger

from utils.utils import Utils


class Worker:
    def __init__(self, utils: Utils):
        self.logger = getLogger(__name__)
        self.logger.info("Initializing worker...")

        self.running = False
        self.utils = utils

    def start(self):
        self.logger.info("Starting worker...")

        self.running = True

        self.logger.info("Worker started!")

        self.process()

    def stop(self):
        self.logger.info("Stopping worker...")

        self.running = False

    def is_running(self):
        return self.running

    def process(self):
        while self.running:
            # Worker continues its processing

            # Get market data
            # Analyze data
            # Generate signals
            # Execute trades

            self.utils.start_heartbeat()
            time.sleep(1)


# import json
# from logging import getLogger

# from utils.config import Configuration


# class Worker:
#     def __init__(self, config: Configuration) -> None:
#         self.logger = getLogger(__name__)
#         self.tickers = []

#         self.logger.info("Initializing worker...")

#         self.config = config

#         # Load tickers from JSON file
#         self.load_tickers()

#     def load_tickers(self):
#         self.tickers = self.config.tickers

#     def print_tickers(self):
#         print("Current tickers:")
#         for ticker in self.tickers:
#             print(ticker)

#     def add_ticker(self):
#         ticker = input("Enter a new ticker: ", end="")
#         self.config.add_ticker(ticker)

#         self.logger.info(f"Added {ticker} to tickers.")

#         # Reload tickers
#         self.load_tickers()

#     def edit_ticker(self):
#         old_ticker = input("Enter the ticker to edit: ")
#         new_ticker = input("Enter the new ticker: ")
#         if old_ticker in self.tickers:
#             index = self.tickers.index(old_ticker)
#             self.tickers[index] = new_ticker
#             self.save_tickers()
#             print(f"Ticker '{old_ticker}' edited successfully.")
#         else:
#             print("Ticker not found.")

#     def remove_ticker(self):
#         ticker = input("Enter the ticker to remove: ", end="")

#         self.config.remove_ticker(ticker)

#         self.logger.info(f"Successfully removed {ticker} from tickers.")

#     def update_market_data(self):
#         # Receive and process the latest market data from the exchange
#         # Update relevant variables, such as price, volume, indicators, etc.
#         pass

#     def make_trading_decisions(self):
#         # Apply trading strategies or algorithms based on market data
#         # Analyze indicators and thresholds to determine buy/sell signals
#         # Consider risk management rules and account constraints
#         pass

#     def execute_trades(self):
#         # Generate trading orders based on trading decisions
#         # Submit buy/sell orders to the exchange's API
#         # Handle order execution errors or rejections
#         pass

#     def update_account(self):
#         # Retrieve updated account information from the exchange
#         # Update local account variables with new balances, positions, etc.
#         pass

#     def wait_for_next_update(self):
#         # Implement a delay or sleep between iterations
#         # Wait for the next market data update interval
#         pass

#     def handle_menu(self):
#         while True:
#             try:
#                 option = int(input("\nEnter option number: "))
#                 if option == 1:
#                     self.print_tickers()
#                 elif option == 2:
#                     self.add_ticker()
#                 elif option == 3:
#                     self.edit_ticker()
#                 elif option == 4:
#                     self.remove_ticker()
#                 elif option == 5:
#                     break
#                 else:
#                     print("Invalid option. Please try again.")
#             except ValueError:
#                 print("Invalid input. Please enter a number.")

#     def run(self):
#         self.logger.info("Running worker...")
#         self.handle_menu()
#         self.logger.info("Worker stopped.")

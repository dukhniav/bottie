import threading

from logging import getLogger

from utils.worker import Worker
from utils.config import Configuration
from utils.utils import Utils
from utils.ticker_manager import TickerManager


class Bottie:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.logger.info("Initializing Bottie...")

        self.config = Configuration()
        self.utils = Utils(self.config)
        self.ticker_manager = TickerManager(self.config)
        self.worker = Worker(self.utils)
        self.worker_thread = None

    def run(self):
        self.logger.info("Starting Bottie...")

        while True:
            # Display menu and get user input
            option = self.display_menu()

            if option == 1:
                self.start_bot()
            elif option == 2:
                self.stop_bot()
            elif option == 3:
                self.view_config()
            elif option == 4:
                self.view_tickers()
            elif option == 5:
                self.add_ticker()
            elif option == 6:
                self.remove_ticker()
            elif option == 0:
                break
            else:
                print("Invalid option. Please try again.")

    def display_menu(self):
        print("Menu:")
        print("1. Start Bot")
        print("2. Stop Bot")
        print("3. View Config")
        print("4. View Current Tickers")
        print("5. Add Ticker")
        print("6. Remove Ticker")
        print("0. Exit")

        try:
            option = int(input("Enter option number: "))
            return option
        except ValueError:
            return 0

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


# import signal
# import time

# from logging import getLogger

# from utils.config import Configuration
# from utils.worker import Worker
# from utils.utils import Utils


# class Bottie:
#     def __init__(self) -> None:
#         self.logger = getLogger(__name__)

#         self.logger.info("Initializing Bottie...")

#         # Setup
#         self.setup()

#         # Initialize necessary variables and connections

#         # connect_to_exchange()
#         # load_account_information()
#         # load_trading_parameters()
#         # subscribe_to_market_data()

#         # Initialize worker
#         self.worker = Worker(self.config)

#     def setup(self):
#         # Initialize config
#         self.logger.info("Entering setup...")
#         self.config = Configuration()

#         # Initialize utils
#         self.utils = Utils(self.config)

#         # Load ENV variables
#         self.logger.info("Loading ENV variables...")

#         # Load trading type
#         if self.config.TRAINING_WHEELS:
#             self.logger.info("Paper trading enabled...")

#             print("Starting bot in paper trading mode.")
#         else:
#             self.logger.info("LIVE trading enabled...")

#             print("Starting bot in LIVE trading mode. Be advised.")

#         # Initialize exchange connection
#         self.exchange = self.config.EXCHANGE
#         self.logger.info(f"Connecting to {self.exchange}")

#         exchange_api = self.exchange.create_api()
#         self.config.get_exchange_credentials(exchange_api.name)

#         # Establish exchange connection
#         self.conn = exchange_api.exchange.establish_connection(
#             self.config.EXCHANGE_API_KEY,
#             self.config.EXCHANGE_API_SECRET,
#             self.config.TRAINING_WHEELS,
#         )

#         # exchange_api.exchange.get_account(self.conn)

#     def handle_signal(self, signum, frame):
#         # Custom signal handler function
#         # Perform any cleanup or necessary actions before exiting
#         self.logger.info("Received termination signal. Stopping worker...")
#         # Perform cleanup actions here (if any)
#         exit(0)

#     def run(self):
#         self.logger.info("Starting Bottie...")
#         # Set the custom signal handler for the termination signal (SIGINT)
#         signal.signal(signal.SIGINT, self.handle_signal)

#         self.logger.info("Bottie started...")

#         # Start worker
#         self.worker.run()
#         # # Get market data

#         # # Analyze data

#         # # Generate signals

#         # # Execute trades

#         # time.sleep(1)
#         # self.utils.start_heartbeat()

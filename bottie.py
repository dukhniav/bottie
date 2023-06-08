import signal
import time

from logging import getLogger

from utils.config import Configuration
from utils.worker import Worker
from utils.utils import Utils


class Bottie:
    def __init__(self) -> None:
        self.logger = getLogger(__name__)

        self.logger.info("Initializing Bottie...")

        # Setup
        self.setup()

        # Initialize necessary variables and connections

        # connect_to_exchange()
        # load_account_information()
        # load_trading_parameters()
        # subscribe_to_market_data()

        # Initialize worker
        self.worker = Worker()

    def setup(self):
        # Initialize config
        self.logger.info("Entering setup...")
        self.config = Configuration()

        # Initialize utils
        self.utils = Utils(self.config)

        # Load ENV variables
        self.logger.info("Loading ENV variables...")

        # Load trading type
        if self.config.TRAINING_WHEELS:
            self.logger.info("Paper trading enabled...")

            print("Starting bot in paper trading mode.")
        else:
            self.logger.info("LIVE trading enabled...")

            print("Starting bot in LIVE trading mode. Be advised.")

        # Initialize exchange connection
        self.exchange = self.config.EXCHANGE
        self.logger.info(f"Connecting to {self.exchange.value}")

        exchange_api = self.exchange.create_api()
        exchange_api.exchange.get_account()

    def handle_signal(self, signum, frame):
        # Custom signal handler function
        # Perform any cleanup or necessary actions before exiting
        self.logger.info("Received termination signal. Stopping worker...")
        # Perform cleanup actions here (if any)
        exit(0)

    def run(self):
        self.logger.info("Starting Bottie...")
        # Set the custom signal handler for the termination signal (SIGINT)
        signal.signal(signal.SIGINT, self.handle_signal)

        self.logger.info("Bottie started...")

        while True:
            # Worker continues its processing
            print("Worker is running...")

            # Get market data

            # Analyze data

            # Generate signals

            # Execute trades

            time.sleep(1)
            self.utils.start_heartbeat()

import logging
import threading
import time

from typing import Any, Dict

from bottie import __version__

from bottie.apis.finnhub_api import Finnhub

from bottie.managers.account_manager import AccountManager
from bottie.managers.transaction_manager import TransactionManager

from bottie.enums.order_side import OrderSide
from bottie.enums.state import State
from bottie.enums.order_type import OrderType

from bottie.smarts import NeuralNetwork
from bottie.smarts import ReplayMemory

from bottie.strategies import GDPGStrategy
from bottie.configuration.configuration import config

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, finnhub_api: Finnhub, account_manager: AccountManager, transactions_manager: TransactionManager) -> None:
        logger.info(f"Initializing worker (ver={__version__})")
        self._stop_event = threading.Event()
        self._worker_thread = None
        self.account = account_manager.get_account_by_name()
        self.transactions = transactions_manager
        self.finnhub = finnhub_api  # Variable to hold the market data source
        self.tickers = config.get_tickers()
        self._state = State.STOPPED
        self.strategy = self.get_strategy()

        # test market data to get dimensions
        test_md = finnhub_api.get_quote("AAPL")

        # Example calculation of input and output dimensions
        # Assuming market_data is a vector of features
        input_dim = len(test_md)
        output_dim = 3  # Assuming you have 3 possible actions: Buy, Sell, Hold

        # Initialize the neural network for the GDPG strategy
        self.policy_network = NeuralNetwork(input_dim, output_dim)

        # Initialize the replay memory for experience replay
        self.replay_memory = ReplayMemory(capacity=10000)

    def start(self) -> bool:
        logger.info("Starting worker...")
        self._state = State.RUNNING
        self._worker_loop()
        return True

    def stop(self) -> bool:
        logger.info("Stopping worker...")
        self._state = State.STOPPED
        return True

    def get_strategy(self) -> GDPGStrategy:
        input_dim = 3
        output_dim = 3
        strategy = GDPGStrategy(input_dim=input_dim, output_dim=output_dim)
        return strategy

    def _worker_loop(self):
        while self._state == State.RUNNING:
            # Retrieve market data from the data source (Finnhub API)
            for ticker in self.tickers:
                market_data = self.finnhub.get_quote(ticker)

                if market_data:
                    # Perform analysis on market data
                    signal = self.analyze_market_data(market_data)

                    # Store transition in replay memory
                    self.store_transition(market_data, signal)

                    # Sample a batch from replay memory
                    state_batch, action_batch, reward_batch, next_state_batch, done_batch = self.replay_memory.sample_batch(
                        batch_size=32)

                    # Update the policy network using the sampled batch
                    self.update_policy_network(
                        state_batch, action_batch, reward_batch, next_state_batch, done_batch)

                    # Generate orders using the policy network
                    orders = self.generate_orders(market_data)

                    # Execute the generated orders
                    self.execute_orders(orders)
                else:
                    logger.debug("Unable to retrieve market data")

            time.sleep(10)  # Sleep for some time before the next iteration

        logger.info("Worker stopped.")

    def store_transition(self, state, action):
        # Store the transition in replay memory
        reward = self.calculate_reward(state, action)
        next_state = self.get_next_state(state, action)
        done = self.is_done(state, action)
        self.replay_memory.store_transition(
            state, action, reward, next_state, done)

    def update_policy_network(self, state_batch, action_batch, reward_batch, next_state_batch, done_batch):
        # Update the policy network using the Gated Deterministic Policy Gradient algorithm
        actor_gradient = self.calculate_actor_gradient(
            state_batch, action_batch)
        critic_targets = self.calculate_critic_targets(
            state_batch, reward_batch, next_state_batch, done_batch)
        self.policy_network.update_weights(actor_gradient, critic_targets)

    def calculate_reward(self, state, action):
        # Calculate the reward for the given state-action pair
        # Implement your own reward function here
        reward = 0  # Placeholder reward, modify according to your strategy
        return reward

    def get_next_state(self, state, action):
        # Calculate and return the next state based on the current state and action
        # Implement the logic to generate the next state based on your strategy
        next_state = None  # Placeholder next state, modify according to your strategy
        return next_state

    def is_done(self, state, action):
        # Determine if the episode is done based on the current state and action
        # Implement the logic to determine episode termination based on your strategy
        done = False  # Placeholder value, modify according to your strategy
        return done

    def calculate_actor_gradient(self, state_batch, action_batch):
        # Calculate the gradient for the actor network using the given state and action batch
        # Implement the logic to calculate the actor gradient based on your strategy
        actor_gradient = None  # Placeholder value, modify according to your strategy
        return actor_gradient

    def calculate_critic_targets(self, state_batch, reward_batch, next_state_batch, done_batch):
        # Calculate the critic targets for the given state, reward, next_state, and done batch
        # Implement the logic to calculate the critic targets based on your strategy
        critic_targets = None  # Placeholder value, modify according to your strategy
        return critic_targets

    def generate_orders(self, market_data):
        # Preprocess the market data if needed
        state = self.preprocess_state(market_data)
        action_probs = self.policy_network.predict(state)
        # Implement your logic to convert action probabilities into orders
        orders = convert_action_probs_to_orders(action_probs)
        return orders

    def analyze_market_data(self, market_data) -> Dict:
        logger.debug(
            f"Analyzing market data for ticker: {market_data['ticker']}")

        # Extract relevant information from market data
        ticker = market_data['ticker']
        price = market_data['price']
        timestamp = market_data['timestamp']

        # Get historical market data for the ticker
        historical_data = self.finnhub.get_historical_data(
            ticker, start_date='2022-01-01', end_date='2022-12-31')

        # Calculate technical indicators
        sma_50 = self.calculate_sma(historical_data, window=50)
        sma_200 = self.calculate_sma(historical_data, window=200)

        # Determine the signal based on the analysis
        signal = None
        if price > sma_50 and price > sma_200:
            signal = {
                'ticker': ticker,
                'signal_type': OrderSide.BUY,
                'price': price,
                'timestamp': timestamp
            }
        elif price < sma_50 and price < sma_200:
            signal = {
                'ticker': ticker,
                'signal_type': OrderSide.SELL,
                'price': price,
                'timestamp': timestamp
            }

        return signal

    def calculate_sma(self, data, window):
        # Calculate the Simple Moving Average (SMA) for the given data and window size
        if len(data) < window:
            return None
        sma = sum(data[-window:]) / window
        return sma

    def execute_orders(self, orders):
        # Execute the generated orders
        # Implement the logic to execute the orders based on your strategy
        if orders:
            # Example: Print the order details
            ticker = orders['ticker']
            _type: OrderType = orders['order_type']
            side: OrderSide = orders['action']
            quantity = orders['quantity']
            price = 0 if _type == OrderType.MARKET else orders['price']

            logger.info(
                f"Executing {_type}-{side} order for {quantity} of {ticker}")
            # Execute the order using the appropriate API or method
            # Logging the execution status
            status = ''

            status = self.transactions.create_transaction(
                ticker, quantity, price)
            if status == 'TransactionType.PENDING':
                status = self.transactions.process_transactions()

                if status == 'TransactionType.PROCESSED':
                    logger.info(f"Order executed successfully: {orders}")
                else:
                    logger.info(f"Transaction failed to process.")
            else:
                logger.debug("Failed to create transaction")

    def convert_action_probs_to_orders(self, action_probs):
        orders = []
        for i, prob in enumerate(action_probs):
            # Determine the action based on the action probabilities
            if prob > 0.5:
                action = OrderSide.BUY
            else:
                action = OrderSide.SELL

            # Create an order dictionary
            order = {
                # Replace with the appropriate ticker symbol
                'ticker': self.tickers[i],
                'order_type': OrderType.LIMIT,  # Replace with the desired order type
                'action': action,
                'quantity': 100,  # Replace with the desired quantity
                'price': 0  # Replace with the desired price or leave it as 0 for market orders
            }
            orders.append(order)

        return orders

    def update_policy_network(self, state_batch, action_batch, reward_batch, next_state_batch, done_batch):
        actor_gradient = self.gdpg_strategy.calculate_actor_gradient(
            state_batch, action_batch)
        critic_targets = self.gdpg_strategy.calculate_critic_targets(
            state_batch, reward_batch, next_state_batch, done_batch)
        self.policy_network.update_weights(actor_gradient, critic_targets)

    def generate_orders(self, market_data):
        orders = self.gdpg_strategy.generate_orders(market_data)
        return orders

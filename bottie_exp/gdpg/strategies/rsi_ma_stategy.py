import numpy as np
import pandas as pd

RSI_LOW = 30
RSI_HIGH = 70
RSI_PERIOD = 14
MA_PERIOD = 50


class RSI_MA_Strategy:
    def __init__(self, rsi_period=RSI_PERIOD, ma_period=MA_PERIOD):
        self.rsi_period = rsi_period
        self.ma_period = ma_period
        self.model = None
        self.total_reward = 0

    def calculate_rsi(self, prices):
        if len(prices) < self.rsi_period:
            return 50  # Return a neutral RSI value

        deltas = np.diff(prices)
        gains = deltas.copy()
        losses = deltas.copy()
        gains[gains < 0] = 0
        losses[losses > 0] = 0
        avg_gain = np.mean(gains[:self.rsi_period])
        avg_loss = np.mean(np.abs(losses[:self.rsi_period]))

        # Check for division by zero
        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_ma(self, prices):
        return np.mean(prices[-self.ma_period:])

    def analyze_data(self, data):
        signals = []
        prices = data.get('c')

        rsi_values = []
        ma_values = []

        for i in range(len(data)):
            rsi = self.calculate_rsi(prices[:i+1])
            rsi_values.append(rsi)

            ma = self.calculate_ma(prices[:i+1])
            ma_values.append(ma)

            # if rsi < 40:
            #     print(f'i: {i} - rsi: {rsi} - ma: {ma} - price: ${prices[i]}')
            if i < self.ma_period:
                signals.append('Hold')  # Wait until we have enough data for MA

            else:
                if rsi > RSI_HIGH and prices[i] > ma:
                    signals.append('Sell')
                elif rsi < RSI_LOW and prices[i] < ma:
                    signals.append('Buy')
                else:
                    signals.append('Hold')

        data['RSI'] = rsi_values
        data['MA'] = ma_values
        data['Signal'] = signals
        return data

    def train(self, states, actions, rewards):
        # Perform training using the provided states, actions, and rewards
        # Update the strategy's model and parameters based on the training process
        # You can define your training logic here

        # Example training code:
        self.total_reward = np.sum(rewards)
        # Update the model or parameters based on the training process
        # self.model.fit(states, actions, rewards)

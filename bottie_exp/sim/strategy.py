import pandas as pd


class Strategy:
    def __init__(self, rsi_period, moving_avg_short, moving_avg_long):
        self.rsi_period = rsi_period
        self.moving_avg_short = moving_avg_short
        self.moving_avg_long = moving_avg_long

    def generate_signals(self, data):
        # Calculate RSI
        data['delta'] = data['close'].diff()
        data['gain'] = data['delta'].where(data['delta'] > 0, 0)
        data['loss'] = -data['delta'].where(data['delta'] < 0, 0)
        data['avg_gain'] = data['gain'].rolling(window=self.rsi_period).mean()
        data['avg_loss'] = data['loss'].rolling(window=self.rsi_period).mean()
        data['rs'] = data['avg_gain'] / data['avg_loss']
        data['rsi'] = 100 - (100 / (1 + data['rs']))

        # Calculate moving averages
        data['short_ma'] = data['close'].rolling(
            window=self.moving_avg_short).mean()
        data['long_ma'] = data['close'].rolling(
            window=self.moving_avg_long).mean()

        # Generate signals
        signals = []
        for i in range(len(data)):
            signal = 0  # Hold signal by default

            # RSI signal
            if data['rsi'][i] > 70:
                signal = -1  # Overbought, sell signal
            elif data['rsi'][i] < 30:
                signal = 1  # Oversold, buy signal

            # Moving average crossover signal
            if data['short_ma'][i] > data['long_ma'][i]:
                signal = 1  # Short MA crosses above long MA, buy signal
            elif data['short_ma'][i] < data['long_ma'][i]:
                signal = -1  # Short MA crosses below long MA, sell signal

            signals.append(signal)

        data['signal'] = signals
        return data


# Example usage
# Assuming you have a DataFrame called 'stock_data' with columns: 'date', 'close'
# Set the desired parameters for the strategy
rsi_period = 14
moving_avg_short = 50
moving_avg_long = 200

# Initialize the strategy
strategy = Strategy(rsi_period, moving_avg_short, moving_avg_long)

# Generate signals
signals = strategy.generate_signals(stock_data)

# Print the signals DataFrame
print(signals)

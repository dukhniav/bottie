import numpy as np
import tensorflow as tf
import json
from gdpg_model import GDPGModel
from gdpg_strategy import GDPGStrategy
from tqdm import tqdm


def handle_format_error(value, format_string):
    try:
        return f"{value:{format_string}}"
    except (TypeError, ValueError):
        return str(value)


def handle_key_error(dictionary, key, fallback_value=None):
    try:
        return dictionary[key]
    except KeyError:
        return fallback_value


def fetch_stock_data(features_shape, file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    dates = sorted(data.keys())
    closing_prices = [float(data[date]["4. close"]) for date in dates]
    volumes = [int(data[date]["6. volume"]) for date in dates]
    opening_prices = [float(data[date]["1. open"]) for date in dates]

    # Preprocess and normalize the features
    closing_prices = np.array(closing_prices)
    closing_prices = (closing_prices - np.min(closing_prices)) / \
        (np.max(closing_prices) - np.min(closing_prices))

    volumes = np.array(volumes)
    volumes = (volumes - np.min(volumes)) / (np.max(volumes) - np.min(volumes))

    opening_prices = np.array(opening_prices)
    opening_prices = (opening_prices - np.min(opening_prices)) / \
        (np.max(opening_prices) - np.min(opening_prices))

    # Combine the features into a single state representation
    states = np.column_stack((closing_prices, volumes, opening_prices))

    # Return only the last quarter of the states
    # Get the length of a quarter of the data
    quarter_length = len(states) // 15
    # Include extra features_shape - 1 for correct indexing
    states = states[-quarter_length - features_shape + 1:]

    return states


def main():
    # Initialize hyperparameters
    features_shape = 3  # Dimension of state space
    actions_shape = 1  # Dimension of action space
    hidden_units = 64  # Number of units in hidden layers
    learning_rate = 0.001  # Learning rate for the optimizer

    # Load the trained model

    model_file = 'models/gdpg_model.h5'
    strategy = GDPGStrategy(features_shape, actions_shape,
                            hidden_units, learning_rate)
    strategy.model.load_weights(model_file)

    # Fetch stock data
    file_path = 'stock_data.json'
    stock_data = fetch_stock_data(features_shape, file_path)

    # Test the GDPG trading strategy
    print("Testing...")
    balance = 1000
    results = []
    transactions = []  # List to store transaction details

    pbar = tqdm(total=len(stock_data) - features_shape + 1)
    stock_balance = 0
    trx = False

    for i in range(features_shape - 1, len(stock_data) - 1):
        state = stock_data[i - features_shape + 1:i + 1, :]

        decision = strategy.model.predict(
            np.expand_dims(state, axis=0), verbose=0)
        price = decision[0, 0]

        # Calculate quantity based on available balance and current price
        quantity = balance / price
        total = quantity * price

        # Log the transaction details
        if decision[0, 0] > 0 and balance > 0:
            if balance >= total:
                trx = True
                action = "BUY"
                balance -= total
                stock_balance += quantity
        else:
            if stock_balance > 0 and stock_balance >= quantity:
                trx = True
                action = "SELL"
                total = quantity * price
                balance += total
                stock_balance -= quantity

        if trx:
            # Save the transaction details in the desired format
            transaction = {
                # Assuming the last column of stock_data represents the date
                "date": stock_data[i][-1],
                "action": action,
                "price": price,
                "quantity": quantity,
                "total": total,
                "balance": balance
            }
            transactions.append(transaction)

            results.append((state, decision, price))

            trx = False
        pbar.update(1)

    pbar.close()

    # Define the file path to save the results
    results_file = 'test_results.txt'
    trans_file = 'test_transactions.txt'

    # Print the results and save them to a file
    # Calculate and print the overall performance metrics
    total_trades = len(results)
    positive_trades = len([trade for trade in results if trade[2] > 0])
    negative_trades = len([trade for trade in results if trade[2] < 0])
    average_profit = sum([trade[2] for trade in results]) / \
        total_trades if total_trades > 0 else 0
    average_profit = handle_format_error(average_profit, ".2f")

    print("=" * 40 + "\n")
    print("Overall Performance Metrics:")
    print(f"Total Trades: {total_trades}")
    print(f"Positive Trades: {positive_trades}")
    print(f"Negative Trades: {negative_trades}")
    print(f"Average Profit: {average_profit}")

    with open(trans_file, 'w') as file:
        for transaction in transactions:
            t_date = handle_key_error(transaction, 'date', '')
            t_action = handle_key_error(transaction, 'action', '')
            t_price = handle_format_error(
                handle_key_error(transaction, 'price'), ".2f")
            t_qty = handle_format_error(
                handle_key_error(transaction, 'quantity'), ".2f")
            t_total = handle_format_error(
                handle_key_error(transaction, 'total'), ".2f")
            t_balance = handle_format_error(
                handle_key_error(transaction, 'balance'), ".2f")

            file.write(
                f"- {t_date} - {t_action} - Price=${t_price} - QTY={t_qty} - Total=${t_total} - Bal=${t_balance}\n")
    print("\nTransactions saved to:", trans_file)

    with open(results_file, 'w') as file:
        file.write("=" * 40 + "\n")
        file.write("Overall Performance Metrics:\n")
        file.write(f"Total Trades: {total_trades}\n")
        file.write(f"Positive Trades: {positive_trades}\n")
        file.write(f"Negative Trades: {negative_trades}\n")
        file.write(f"Average Profit: {average_profit}\n")
    print("\nResults saved to:", results_file)

    # Clear the TensorFlow computational graph and release GPU memory
    tf.keras.backend.clear_session()


if __name__ == '__main__':
    main()

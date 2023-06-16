from datetime import datetime
import numpy as np
import tensorflow as tf
import optuna
import json

from gdpg_strategy import GDPGStrategy

# Training loop
TRAIN_EPOCHS = 10  # Number of training epochs
BATCH_SIZE = 32  # Batch size for each training iteration

# Create an instance of the GDPGStrategy
FEATURES_SHAPE = 8  # Example dimension for the state
ACTIONS_SHAPE = 2  # Example dimension for the action
HIDDEN_UNITS = 64  # Number of hidden units in the model
LEARNING_RATE = 0.001  # Learning rate for the optimizer


def load_historical_data(file_path, batch_size):
    with open(file_path, 'r') as file:
        data = json.load(file)

    states = []
    actions = []
    rewards = []

    batch_states = []
    batch_actions = []
    batch_rewards = []

    for date, values in data.items():
        # Extract the relevant data from the JSON file
        open_price = float(values['1. open'])
        high_price = float(values['2. high'])
        low_price = float(values['3. low'])
        close_price = float(values['4. close'])
        adjusted_close = float(values['5. adjusted close'])
        volume = int(values['6. volume'])
        dividend_amount = float(values['7. dividend amount'])
        split_coefficient = float(values['8. split coefficient'])

        # Define the state and action based on the extracted data
        state = [open_price, high_price, low_price, close_price,
                 adjusted_close, volume, dividend_amount, split_coefficient]
        action = 1 if close_price < open_price else - \
            1  # Modify the action logic as needed

        # Calculate the reward based on your trading strategy's logic
        previous_close = states[-1][3] if states else open_price
        # Example reward calculation, modify as needed
        reward = close_price - previous_close

        # Append the state, action, and reward to the respective batches
        batch_states.append(state)
        batch_actions.append(action)
        batch_rewards.append(reward)

        # If the batch is full, add it to the main lists and reset the batch
        if len(batch_states) == batch_size:
            states.extend(batch_states)
            actions.extend(batch_actions)
            rewards.extend(batch_rewards)
            batch_states = []
            batch_actions = []
            batch_rewards = []

    # Add any remaining data in the last batch
    if batch_states:
        states.extend(batch_states)
        actions.extend(batch_actions)
        rewards.extend(batch_rewards)

    return states, actions, rewards


def objective(trial):
    # Define the search space for hyperparameters
    # trial.suggest_int("features_shape", 2, 10)
    features_shape = FEATURES_SHAPE
    actions_shape = ACTIONS_SHAPE  # trial.suggest_int("actions_shape", 1, 5)
    hidden_units = trial.suggest_int("hidden_units", 32, 128)
    learning_rate = trial.suggest_float('learning_rate', 0.001, 0.1, log=True)

    # Create the GDPG trading strategy
    strategy = GDPGStrategy(
        features_shape, actions_shape, hidden_units, learning_rate)

    # Load and process historical data
    states, actions, rewards = load_historical_data(
        'stock_data.json', BATCH_SIZE)

    # Convert the data to numpy arrays
    states = np.array(states)
    actions = np.array(actions)
    rewards = np.array(rewards)

    num_samples = states.shape[0]
    num_batches = num_samples // BATCH_SIZE

    for epoch in range(TRAIN_EPOCHS):
        # Shuffle the data for each epoch
        indices = np.arange(num_samples)
        np.random.shuffle(indices)
        shuffled_states = states[indices]
        shuffled_actions = actions[indices]
        shuffled_rewards = rewards[indices]

        # Perform training in batches
        for batch in range(num_batches):
            start = batch * BATCH_SIZE
            end = (batch + 1) * BATCH_SIZE

            # Extract a batch of data
            batch_states = shuffled_states[start:end]
            batch_actions = shuffled_actions[start:end]
            batch_rewards = shuffled_rewards[start:end]

            # Train the strategy on the batch
            strategy.train(batch_states, batch_actions, batch_rewards)

    # Calculate the metric to optimize (e.g., reward, accuracy, etc.)
    metric = calculate_metric(strategy)  # Change this to the desired metric

    # Save the best model based on the metric
    if trial.should_prune() or metric < 0:  # Prune unpromising trials or trials with negative metric
        raise optuna.TrialPruned()
    else:
        strategy.model.save_weights('models/gdpg_model.h5')

    return metric


def calculate_metric(strategy):
    total_reward = strategy.total_reward.numpy()

    # You can apply any transformation or calculation to the total reward
    metric = total_reward

    return metric


# Run the optimization
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100)

# Print the best parameters and the corresponding metric
best_params = study.best_params
best_metric = study.best_value

print("Best Parameters:", best_params)
print("Best Metric:", best_metric)

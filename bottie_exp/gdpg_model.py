import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


class GDPGModel:
    def __init__(self, state_dim, action_dim, hidden_units):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_units = hidden_units

        # Create the model architecture
        self.model = Sequential()
        self.model.add(Dense(hidden_units, activation='relu',
                       input_shape=(state_dim,)))
        self.model.add(Dense(hidden_units, activation='relu'))
        self.model.add(Dense(hidden_units, activation='relu'))
        self.model.add(Dense(action_dim, activation='linear'))

        # Compile the model
        self.model.compile(optimizer='adam', loss='mse')

    def get_action(self, state):
        return self.model.predict(state)

    def load_weights(self, file_path):
        self.model.load_weights(file_path)

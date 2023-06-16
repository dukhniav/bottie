import tensorflow as tf
from tensorflow import keras
from keras import layers


class NeuralNetwork:
    """
    NeuralNetwork represents a deep neural network used in reinforcement learning algorithms.

    Args:
        input_dim (int): Dimensionality of the input space.
        output_dim (int): Dimensionality of the output space.

    Attributes:
        input_dim (int): Dimensionality of the input space.
        output_dim (int): Dimensionality of the output space.
        model (tf.keras.Model): The neural network model.

    Methods:
        build_model(): Builds the neural network model.
        update_weights(actor_gradient, critic_targets): Updates the weights of the neural network.
        predict(state): Predicts action probabilities given a state.
    """

    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.model = self.build_model()

    def build_model(self):
        """
        Builds the neural network model.

        Returns:
            tf.keras.Model: The constructed neural network model.
        """
        model = keras.Sequential()
        model.add(layers.Dense(64, activation='relu', input_dim=self.input_dim))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(self.output_dim, activation='softmax'))
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        return model

    def update_weights(self, actor_gradient, critic_targets):
        """
        Updates the weights of the neural network using the calculated actor gradient and critic targets.

        Args:
            actor_gradient: The gradient of the actor network.
            critic_targets: The targets for the critic network.

        Returns:
            None
        """
        self.model.train_on_batch(actor_gradient, critic_targets)

    def predict(self, state):
        """
        Predicts action probabilities given a state.

        Args:
            state: The input state.

        Returns:
            numpy.ndarray: Action probabilities predicted by the neural network.
        """
        return self.model.predict(state)

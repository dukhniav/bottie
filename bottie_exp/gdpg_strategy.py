import tensorflow as tf
import numpy as np


class GDPGStrategy:
    def __init__(self, state_dim, action_dim, hidden_units, learning_rate):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_units = hidden_units
        self.learning_rate = learning_rate

        # Build the model
        self.model = self.build_model()

        # Define the loss function
        self.loss_object = tf.keras.losses.MeanSquaredError()

        # Define the optimizer
        self.optimizer = tf.keras.optimizers.Adam(
            learning_rate=self.learning_rate)

        # Define metrics for tracking training progress
        self.loss_metric = tf.keras.metrics.Mean()
        self.accuracy_metric = tf.keras.metrics.BinaryAccuracy()
        self.reward_tracker = tf.keras.metrics.Sum()
        self.risk_tracker = tf.keras.metrics.Mean()

        # Variable to track the total accumulated reward
        self.total_reward = tf.Variable(0.0, dtype=tf.float32)

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(
                self.hidden_units, activation='relu', input_shape=(self.state_dim,)),
            tf.keras.layers.Dense(self.hidden_units, activation='relu'),
            tf.keras.layers.Dense(self.action_dim, activation='linear')
        ])
        return model

    @tf.function
    def train_step(self, states, actions, rewards):
        with tf.GradientTape() as tape:
            logits = self.model(states, training=True)
            reshaped_actions = tf.reshape(actions, [-1, 1])
            loss_value = self.loss_object(reshaped_actions, logits)

        gradients = tape.gradient(loss_value, self.model.trainable_variables)
        self.optimizer.apply_gradients(
            zip(gradients, self.model.trainable_variables))

    def train(self, states, actions, rewards):
        self.train_step(states, actions, rewards)

    @property
    def loss(self):
        return self.loss_metric.result()

    @property
    def accuracy(self):
        return self.accuracy_metric.result()

    @property
    def reward(self):
        return self.reward_tracker.result()

    @property
    def risk(self):
        return self.risk_tracker.result()

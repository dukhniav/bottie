import random
from collections import deque
from typing import Tuple


class ReplayMemory:
    """
    ReplayMemory is used to store and sample transitions for experience replay in reinforcement learning algorithms.

    Args:
        capacity (int): Maximum number of transitions that the memory can store.

    Attributes:
        capacity (int): Maximum capacity of the memory.
        memory (deque): Deque to store the transitions.

    Methods:
        store_transition(state: Tuple, action: int, reward: float, next_state: Tuple, done: bool): Stores a transition in the memory.
        sample_batch(batch_size: int) -> Tuple: Samples a batch of transitions from the memory.
        is_full() -> bool: Checks if the memory is full.
        __len__() -> int: Returns the current size of the memory.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.memory = deque(maxlen=capacity)

    def store_transition(self, state: Tuple, action: int, reward: float, next_state: Tuple, done: bool):
        """
        Stores a transition (state, action, reward, next_state, done) in the replay memory.

        Args:
            state (Tuple): Current state of the environment.
            action (int): Action taken in the current state.
            reward (float): Reward received for the action in the current state.
            next_state (Tuple): Next state after taking the action.
            done (bool): Flag indicating if the episode terminated after the action.

        Returns:
            None
        """
        transition = (state, action, reward, next_state, done)
        self.memory.append(transition)

    def sample_batch(self, batch_size: int) -> Tuple:
        """
        Samples a batch of transitions from the replay memory.

        Args:
            batch_size (int): Number of transitions to sample.

        Returns:
            Tuple: Batch of sampled transitions in the form (state_batch, action_batch, reward_batch, next_state_batch, done_batch).
        """
        batch = random.sample(self.memory, batch_size)
        state_batch, action_batch, reward_batch, next_state_batch, done_batch = zip(
            *batch)
        return state_batch, action_batch, reward_batch, next_state_batch, done_batch

    def is_full(self) -> bool:
        """
        Checks if the replay memory is full.

        Returns:
            bool: True if the memory is full, False otherwise.
        """
        return len(self.memory) == self.capacity

    def __len__(self) -> int:
        """
        Returns the current size of the replay memory.

        Returns:
            int: Current size of the memory.
        """
        return len(self.memory)

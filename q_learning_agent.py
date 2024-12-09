import numpy as np
import random

class QLearningAgent:
    def __init__(self, action_space, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.99):
        self.q_table = {}
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

    def choose_action(self, state, possible_actions):
        if not possible_actions:  # No actions available
            return None
        if np.random.rand() < self.exploration_rate:
            return random.choice(possible_actions)  # Explore
        q_values = [self.q_table.get((state, action), 0) for action in possible_actions]
        max_q = max(q_values)
        return possible_actions[q_values.index(max_q)]  # Exploit


    def learn(self, state, action, reward, next_state, possible_next_actions):
        old_value = self.q_table.get((state, action), 0)
        future_q = max([self.q_table.get((next_state, a), 0) for a in possible_next_actions], default=0)
        self.q_table[(state, action)] = old_value + self.learning_rate * (reward + self.discount_factor * future_q - old_value)

    def decay_exploration(self):
        self.exploration_rate *= self.exploration_decay

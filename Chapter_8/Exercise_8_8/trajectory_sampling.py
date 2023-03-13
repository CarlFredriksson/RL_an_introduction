import numpy as np
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, num_states, num_actions, b):
        self.transitions = []
        for _ in range(num_states):
            t = []
            for _ in range(num_actions):
                t.append(self._init_transitions(num_states, b))
            self.transitions.append(t)

    def _init_transitions(self, num_states, b):
        next_states = np.random.randint(0, num_states, b)
        # The last expected reward is for the transition to the terminal state
        expected_rewards = np.random.normal(size=b+1)
        return next_states, expected_rewards

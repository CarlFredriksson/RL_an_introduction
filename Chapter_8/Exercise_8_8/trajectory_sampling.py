import numpy as np
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, num_states, num_actions, b):
        self.b = b
        self.starting_state = 0
        self.terminal_state = num_states - 1
        self.transitions = []
        for _ in range(num_states):
            action_transitions = []
            for _ in range(num_actions):
                action_transitions.append(self._init_transitions(num_states, b))
            self.transitions.append(action_transitions)

    def _init_transitions(self, num_states, b):
        next_states = np.random.choice(np.arange(num_states), b, False)
        # The last expected reward is for the transition to the terminal state
        expected_rewards = np.random.normal(size=b+1)
        for i in range(b):
            if next_states[i] == self.terminal_state:
                expected_rewards[i] = expected_rewards[-1]
        return next_states, expected_rewards

    def take_action(self, state, action):
        next_states, expected_rewards = self.transitions[state][action]

        # Transition to terminal state with probability 0.1
        if np.random.rand() < 0.1:
            return expected_rewards[-1], self.terminal_state, True
        
        # Randomly select one of b next states
        rand_index = np.random.randint(0, self.b)
        expected_reward = expected_rewards[rand_index]
        next_state = next_states[rand_index]

        return expected_reward, next_state, next_state == self.terminal_state

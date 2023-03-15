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
        
        # Randomly transition to one of b next states
        rand_index = np.random.randint(0, self.b)
        expected_reward = expected_rewards[rand_index]
        next_state = next_states[rand_index]

        return expected_reward, next_state, next_state == self.terminal_state

def arg_max_random_tie_break(x):
     return np.random.choice(np.flatnonzero(x == x.max()))

def eps_greedy_action_selection(Q, state, eps):
    # Select a random action with probability eps
    if np.random.random() < eps:
        return np.random.choice(np.arange(len(Q[state])))
    
    # Select the maximizing action - ties broken randomly
    return arg_max_random_tie_break(Q[state])

def compute_expected_update(Q, transitions, state, action):
    next_states, expected_rewards = transitions[state][action]
    b = len(next_states)
    updated_value = 0
    for i in range(b):
        transition_probability = (1 - 0.1) / b
        updated_value += transition_probability * (expected_rewards[i] + Q[next_states[i]].max())
    updated_value += 0.1 * expected_rewards[-1]
    return updated_value

def compute_start_state_value(environment, Q, num_runs=10000, max_num_steps_per_run=1000000):
    sum_of_expected_rewards = 0
    for _ in range(num_runs):
        state = environment.starting_state
        for _ in range(max_num_steps_per_run):
            action = eps_greedy_action_selection(Q, state, 0)
            expected_reward, state, reached_terminal_state = environment.take_action(state, action)
            sum_of_expected_rewards += expected_reward
            if reached_terminal_state:
                break
    return sum_of_expected_rewards / num_runs

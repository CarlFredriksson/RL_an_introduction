import numpy as np
import random
import matplotlib.pyplot as plt

class Environment:
    def __init__(self):
        self.grid_size = (9,6)
        self.start_state = (3,0)
        self.goal_state = (8,5)
        self.first_wall_states = [(1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2)]
        self.second_wall_states = [(1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2)]
        self.available_actions = (0, 1, 2, 3) # up, down, right, left

    def _check_state_validity(self, state, first_wall_active):
        # Out of bounds
        if state[0] < 0 or state[1] < 0 or state[0] > self.grid_size[0] - 1 or state[1] > self.grid_size[1] - 1:
            return False

        # Inside a wall
        if first_wall_active and state in self.first_wall_states:
            return False
        elif not first_wall_active and state in self.second_wall_states:
            return False

        return True

    def take_action(self, state, action, first_wall_active=True):
        # Move according to action
        state_increment = None
        match action:
            case 0: state_increment = (0,1)
            case 1: state_increment = (0,-1)
            case 2: state_increment = (1,0)
            case 3: state_increment = (-1,0)
            case _: raise ValueError(f"Invalid action '{action}'")
        new_state = (state[0] + state_increment[0], state[1] + state_increment[1])
        if not self._check_state_validity(new_state, first_wall_active):
            new_state = state

        # Check if goal was reached
        reward = 0
        if new_state == self.goal_state:
            reward = 1
            new_state = self.start_state

        return reward, new_state

def eps_greedy_action_selection(Q, state, eps):
    # Select a random action with probability eps
    if np.random.random() < eps:
        return np.random.choice(np.arange(len(Q[state])))
    
    # Select the maximizing action - ties broken randomly
    return np.random.choice(np.flatnonzero(Q[state] == Q[state].max()))

def update_cumulative_reward(cumulative_reward, reward, t):
    prev_cumulative_reward = 0
    if t > 0:
        prev_cumulative_reward = cumulative_reward[t-1]
    cumulative_reward[t] = prev_cumulative_reward + reward
    return cumulative_reward

def run_q_learning(env, num_time_steps, num_time_steps_before_second_wall, eps, learning_rate, gamma):
    cumulative_reward = np.zeros(num_time_steps)
    Q = np.zeros((env.grid_size[0], env.grid_size[1], len(env.available_actions)))
    state = env.start_state
    for t in range(num_time_steps):
        first_wall_active = True if t < num_time_steps_before_second_wall else False
        action = eps_greedy_action_selection(Q, state, eps)
        reward, new_state = env.take_action(state, action, first_wall_active)
        Q[state[0], state[1], action] += learning_rate * (reward + gamma * np.max(Q[new_state]) - Q[state[0], state[1], action])
        state = new_state
        cumulative_reward = update_cumulative_reward(cumulative_reward, reward, t)
    return cumulative_reward

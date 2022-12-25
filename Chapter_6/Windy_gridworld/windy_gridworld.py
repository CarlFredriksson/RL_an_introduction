import numpy as np
import random

class Environment:
    def __init__(self):
        self.min_x = 0
        self.max_x = 9
        self.min_y = 0
        self.max_y = 6
        self.wind_per_col = np.array([0, 0, 0, 1, 1, 1, 2, 2, 1, 0])
        self.terminal_state = (7, 3)
        self.available_actions = ("up", "down", "right", "left")

    def take_action(self, state, action):
        x, y = state

        # Validate state
        if x < self.min_x or x > self.max_x or y < self.min_y or y > self.max_y:
            raise ValueError(f"state '{state}' is not valid")
        
        # Apply wind
        y += self.wind_per_col[x]
        x, y = self._keep_position_within_grid(x, y)

        # Move according to action
        if action == "up":
            y += 1
        elif action == "down":
            y -= 1
        elif action == "right":
            x += 1
        elif action == "left":
            x -= 1
        else:
            raise ValueError(f"action '{action}' is not valid")
        new_state = self._keep_position_within_grid(x, y)

        reward = -1
        reached_terminal_state = new_state == self.terminal_state
        return reward, new_state, reached_terminal_state
    
    def _keep_position_within_grid(self, x, y):
        x = max(min(x, self.max_x), self.min_x)
        y = max(min(y, self.max_y), self.min_y)
        return x, y

class SarsaAgent:
    def __init__(self, step_size, Q_init):
        self.step_size = step_size
        self.Q = Q_init
    
    # Eps-greedy action selection
    def select_action(self, state, available_actions, eps):
        # Select random action with probability eps
        if random.random() < eps:
            return random.choice(available_actions)

        # Select greedy action, ties broken randomly
        max_value = -np.inf
        greedy_actions = []
        for action in available_actions:
            value = self.Q[state][action]
            if value > max_value:
                max_value = value
                greedy_actions = [action]
            elif value == max_value:
                greedy_actions.append(action)
        
        return random.choice(greedy_actions)

    def learn(self, state, action, reward, next_state, next_action):
        self.Q[state][action] += self.step_size * (reward + self.Q[next_state][next_action] - self.Q[state][action])

def run_episode(environment, agent, initial_state, eps, max_num_steps=100000):
    trajectory = []
    state = initial_state
    action = agent.select_action(state, environment.available_actions, eps)
    trajectory.append((state, action))
    for t in range(max_num_steps):
        reward, next_state, reached_terminal_state = environment.take_action(state, action)
        next_action = agent.select_action(next_state, environment.available_actions, eps)
        agent.learn(state, action, reward, next_state, next_action)
        state = next_state
        action = next_action
        trajectory.append((state, action))
        if reached_terminal_state:
            break
    return trajectory
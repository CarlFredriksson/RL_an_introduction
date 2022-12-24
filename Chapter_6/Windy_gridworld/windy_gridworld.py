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

    def take_action(self, state, action):
        x, y = state

        # Validate state
        if x < self.min_x or x > self.max_x or y < self.min_y or y > self.max_y:
            raise ValueError(f"state '{state}' is not valid")
        
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
        x, y = self._keep_position_within_grid(x, y)
        
        # Apply wind
        y += self.wind_per_col[x]
        new_state = self._keep_position_within_grid(x, y)

        reward = -1
        reached_terminal_state = new_state == self.terminal_state
        return reward, new_state, reached_terminal_state
    
    def _keep_position_within_grid(self, x, y):
        x = max(min(x, self.max_x), self.min_x)
        y = max(min(y, self.max_y), self.min_y)
        return x, y

class SarsaAgent:
    def __init__(self, step_size, eps, Q_init):
        self.step_size = step_size
        self.eps = eps
        self.Q = Q_init
    
    # Eps-greedy action selection
    def select_action(self, state, available_actions):
        # Select random action with probability eps
        if random.random() < self.eps:
            return random.choice(available_actions)

        # Select greedy action
        max_val = -np.inf
        greedy_action = None
        for action in available_actions:
            val = self.Q[state][action]
            if val > max_val:
                max_val = val
                greedy_action = action
        
        return greedy_action

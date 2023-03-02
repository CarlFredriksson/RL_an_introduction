import numpy as np
import random
import matplotlib.pyplot as plt

class Environment:
    def __init__(self):
        self.grid_size = np.array([8, 5])
        self.start_state = np.array([3, 0])
        self.goal_state = np.array([8, 5])
        self.available_actions = ("up", "down", "right", "left")

    def take_action(self, state, action):
        state_increment = None
        match action:
            case "up": state_increment = np.array([0, 1])
            case "down": state_increment = np.array([0, -1])
            case "right": state_increment = np.array([1, 0])
            case "left": state_increment = np.array([-1, 0])
            case _: raise ValueError("Invalid action")
        new_state = state + state_increment
        new_state[0] = max(min(new_state[0], self.grid_size[0]), 0)
        new_state[1] = max(min(new_state[1], self.grid_size[1]), 0)
        reward = 0
        if (new_state == self.goal_state).all():
            reward = 1
            new_state = self.start_state
        return reward, new_state

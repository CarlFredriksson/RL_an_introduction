import numpy as np
import random

class Environment:
    def __init__(self):
        self.terminal_state = 0
        self.available_actions = ("up", "down", "right", "left")
        self.transitions = (
            {"up": 0, "down": 0, "right": 0, "left": 0},
            {"up": 1, "down": 5, "right": 2, "left": 0},
            {"up": 2, "down": 6, "right": 3, "left": 1},
            {"up": 3, "down": 7, "right": 3, "left": 2},
            {"up": 0, "down": 8, "right": 5, "left": 4},
            {"up": 1, "down": 9, "right": 6, "left": 4},
            {"up": 2, "down": 10, "right": 5, "left": 7},
            {"up": 3, "down": 11, "right": 7, "left": 6},
            {"up": 4, "down": 12, "right": 9, "left": 8},
            {"up": 5, "down": 13, "right": 10, "left": 8},
            {"up": 6, "down": 14, "right": 11, "left": 9},
            {"up": 7, "down": 0, "right": 11, "left": 10},
            {"up": 8, "down": 12, "right": 13, "left": 12},
            {"up": 9, "down": 13, "right": 14, "left": 12},
            {"up": 10, "down": 14, "right": 0, "left": 13}
        )

    def take_action(self, state, action):
        reward = -1
        new_state = self.transitions[state][action]
        reached_terminal_state = new_state == self.terminal_state
        return reward, new_state, reached_terminal_state
    
    def generate_random_start_state(self):
        return random.randint(1, len(self.transitions) - 1)

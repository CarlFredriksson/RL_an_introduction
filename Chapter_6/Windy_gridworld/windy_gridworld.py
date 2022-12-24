import numpy as np

class Environment:
    def __init__(self):
        self.num_grid_rows = 7
        self.num_grid_cols = 10
        self.wind_per_col = np.array([0, 0, 0, 1, 1, 1, 2, 2, 1, 0])

    def take_action(self, state, action):
        

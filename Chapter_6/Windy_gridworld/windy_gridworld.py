import numpy as np

class Environment:
    def __init__(self):
        self.min_x = 0
        self.max_x = 9
        self.min_y = 0
        self.max_y = 6
        self.wind_per_col = np.array([0, 0, 0, 1, 1, 1, 2, 2, 1, 0])

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
        x, y = self._keep_position_within_grid(x, y)

        return x, y
    
    def _keep_position_within_grid(self, x, y):
        x = max(min(x, self.max_x), self.min_x)
        y = max(min(y, self.max_y), self.min_y)
        return x, y

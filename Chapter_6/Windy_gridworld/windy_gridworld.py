import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import colors

class Environment:
    def __init__(self, allow_diagonal_actions=False):
        self.min_x = 0
        self.max_x = 9
        self.min_y = 0
        self.max_y = 6
        self.wind_per_col = np.array([0, 0, 0, 1, 1, 1, 2, 2, 1, 0])
        self.terminal_state = (7, 3)
        self.available_actions = ("up", "down", "right", "left")
        if allow_diagonal_actions:
            self.available_actions += ("up-right", "up-left", "down-right", "down-left")

    def take_action(self, state, action):
        x, y = state
        wind = self.wind_per_col[x]

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
        elif action == "up-right":
            y += 1
            x += 1
        elif action == "up-left":
            y += 1
            x -= 1
        elif action == "down-right":
            y -= 1
            x += 1
        elif action == "down-left":
            y -= 1
            x -= 1
        else:
            raise ValueError(f"action '{action}' is not valid")
        x, y = self._keep_position_within_grid(x, y)

        # Apply wind
        y += wind
        new_state = self._keep_position_within_grid(x, y)

        reward = -1
        reached_terminal_state = new_state == self.terminal_state
        return reward, new_state, reached_terminal_state
    
    def _keep_position_within_grid(self, x, y):
        x = max(min(x, self.max_x), self.min_x)
        y = max(min(y, self.max_y), self.min_y)
        return x, y

class SarsaAgent:
    def __init__(self, step_size, max_x, max_y, available_actions):
        self.step_size = step_size
        self.Q = {}
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                self.Q[(x, y)] = {}
                for action in available_actions:
                    self.Q[(x, y)][action] = 0
    
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

def train_agent(environment, agent, num_episodes):
    episode_lengths = []
    for ep in range(num_episodes):
        eps = (1 - ep) / num_episodes
        trajectory = run_episode(environment, agent, (0, 3), eps)
        episode_lengths.append(len(trajectory) - 1)
    return episode_lengths

def plot_training(episode_lengths, fig_size, title):
    fig, ax = plt.subplots(figsize=fig_size)
    plt.plot(np.arange(len(episode_lengths)), episode_lengths)
    plt.xlabel("Episode", fontsize="12")
    plt.ylabel("Time steps until terminal state reached", fontsize="12")
    plt.title(title, fontsize=14)
    plt.ylim(0, 100)

def plot_trajectory(trajectory, grid_size, terminal_state, fig_size, title):
    data = np.zeros(grid_size)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if (j, i) == terminal_state:
                data[i, j] = 1
            else:
                data[i, j] = 0
    fig, ax = plt.subplots(figsize=fig_size)
    ax.set_xticks(np.arange(0, grid_size[1], 1))
    ax.set_yticks(np.arange(0, grid_size[0], 1))
    cmap = colors.ListedColormap(["white", "green"])
    plt.pcolormesh(data, edgecolors="k", cmap=cmap)
    x = [trajectory[t][0][0] + 0.5 for t in range(len(trajectory))]
    y = [trajectory[t][0][1] + 0.5 for t in range(len(trajectory))]
    plt.plot(x, y, ".-")
    plt.title(title, fontsize=14)

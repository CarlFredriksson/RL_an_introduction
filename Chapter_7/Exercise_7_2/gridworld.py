import numpy as np
import random
import matplotlib.pyplot as plt

class Environment:
    def __init__(self):
        self.terminal_state = 0
        self.available_actions = ("up", "down", "right", "left")
        self.transitions = (
            {"up": 0, "down": 0, "right": 0, "left": 0}, # Terminal state
            {"up": 1, "down": 5, "right": 2, "left": 0},
            {"up": 2, "down": 6, "right": 3, "left": 1},
            {"up": 3, "down": 7, "right": 3, "left": 2},
            {"up": 0, "down": 8, "right": 5, "left": 4},
            {"up": 1, "down": 9, "right": 6, "left": 4},
            {"up": 2, "down": 10, "right": 7, "left": 5},
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

def compute_rms_error(V):
    v_truth = np.array([0, -14, -20, -22, -14, -18, -20, -20, -20, -20, -18, -14, -22, -20, -14])
    return np.sqrt(np.sum(np.power(V - v_truth, 2)) / len(V))

def run_td_0(environment, num_episodes, max_num_steps_per_episode, step_size):
    V = np.zeros(len(environment.transitions))
    rms_error_per_episode = np.zeros(num_episodes)
    for ep in range(num_episodes):
        state = environment.generate_random_start_state()
        for t in range(max_num_steps_per_episode):
            action = random.choice(environment.available_actions)
            reward, new_state, reached_terminal_state = environment.take_action(state, action)
            V[state] += step_size * (reward + V[new_state] - V[state])
            state = new_state
            if reached_terminal_state:
                break
        rms_error_per_episode[ep] = compute_rms_error(V)
    return V, rms_error_per_episode

def run_n_step_td(environment, num_episodes, max_num_steps_per_episode, step_size, n):
    V = np.zeros(len(environment.transitions))
    rms_error_per_episode = np.zeros(num_episodes)
    for ep in range(num_episodes):
        rewards = []
        states = [environment.generate_random_start_state()]
        T = np.inf
        for t in range(max_num_steps_per_episode):
            if t < T:
                action = random.choice(environment.available_actions)
                reward, new_state, reached_terminal_state = environment.take_action(states[t], action)
                rewards.append(reward)
                states.append(new_state)
                if reached_terminal_state:
                    T = t + 1
            tau = t - n + 1
            if tau >= 0:
                G = np.sum(rewards[tau:min(tau + n, T)])
                if tau + n < T:
                    G = G + V[states[tau + n]]
                V[states[tau]] += step_size * (G - V[states[tau]])
            if tau == T - 1:
                break
        rms_error_per_episode[ep] = compute_rms_error(V)
    return V, rms_error_per_episode

def run_n_step_sum_td_errors(environment, num_episodes, max_num_steps_per_episode, step_size, n):
    V = np.zeros(len(environment.transitions))
    rms_error_per_episode = np.zeros(num_episodes)
    for ep in range(num_episodes):
        td_errors = []
        states = [environment.generate_random_start_state()]
        T = np.inf
        for t in range(max_num_steps_per_episode):
            if t < T:
                action = random.choice(environment.available_actions)
                reward, new_state, reached_terminal_state = environment.take_action(states[t], action)
                td_errors.append(reward + V[new_state] - V[states[t]])
                states.append(new_state)
                if reached_terminal_state:
                    T = t + 1
            tau = t - n + 1
            if tau >= 0:
                V[states[tau]] += step_size * np.sum(td_errors[tau:min(tau + n, T)])
            if tau == T - 1:
                break
        rms_error_per_episode[ep] = compute_rms_error(V)
    return V, rms_error_per_episode

def plot_progress(rms_error_per_episode, fig_size, title):
    fig, ax = plt.subplots(figsize=fig_size)
    plt.plot(np.arange(len(rms_error_per_episode)), rms_error_per_episode)
    plt.xlabel("Episode", fontsize="12")
    plt.ylabel("RMS Error", fontsize="12")
    plt.title(title, fontsize=14)

def plot_results(fig_size, results, labels):
    fig, ax = plt.subplots(figsize=fig_size)
    for i in range(len(results)):
        plt.plot(np.arange(len(results[i])), results[i], label=labels[i])
    plt.xlabel("Episode", fontsize="12")
    plt.ylabel("RMS Error", fontsize="12")
    plt.title("Gridworld Experiment", fontsize=14)
    plt.legend()

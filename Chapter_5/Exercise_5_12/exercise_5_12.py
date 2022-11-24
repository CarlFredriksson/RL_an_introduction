import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random
from skimage.draw import line

def plot_map(starting_line, finishing_line, track, grid_size, fig_size):
    data = np.zeros(grid_size)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if (j, i) in track:
                data[i, j] = 1
            elif (j, i) in starting_line:
                data[i, j] = 2
            elif(j, i) in finishing_line:
                data[i, j] = 3
    fig, ax = plt.subplots(figsize=fig_size)
    ax.set_xticks(np.arange(0, grid_size[1], 1))
    ax.set_yticks(np.arange(0, grid_size[0], 1))
    cmap = colors.ListedColormap(["black", "white", "red", "green"])
    plt.pcolormesh(data, edgecolors="k", cmap=cmap)

def plot_trajectory(starting_line, finishing_line, track, grid_size, fig_size, states):
    plot_map(starting_line, finishing_line, track, grid_size, fig_size)
    x = []
    y = []
    for i in range(len(states)):
        x.append(states[i][0] + 0.5)
        y.append(states[i][1] + 0.5)
    plt.plot(x, y, "-o")

def get_available_actions(state):
     available_actions = []
     x, y, v_x, v_y = state
     for v_x_inc in (-1, 0, 1):
          v_x_new = v_x + v_x_inc
          for v_y_inc in (-1, 0, 1):
               v_y_new = v_y + v_y_inc
               if not (v_x_new < 0 or v_y_new < 0 or v_x_new > 5 or v_y_new > 5 or
                    (v_x_new == 0 and v_y_new == 0)):
                    available_actions.append((v_x_inc, v_y_inc))
     return available_actions

def get_eps_greedy_probabilities(state, greedy_action, eps=0):
    probabilities = {}
    available_actions = get_available_actions(state)
    num_available_actions = len(available_actions)
    for action in available_actions:
        probabilities[action] = eps / num_available_actions
        if action == greedy_action:
            probabilities[action] += 1 - eps
    return probabilities

def generate_start_state(starting_line):
    start_x, start_y = random.choice(list(starting_line))
    return start_x, start_y, 0, 0

def initialize_learning(starting_line, track, eps):
    policy = {}
    Q = {}
    N = {}
    for x, y in starting_line.union(track):
        for v_x in range(6):
            for v_y in range(6):
                state = (x, y, v_x, v_y)
                available_actions = get_available_actions(state)
                policy[state] = get_eps_greedy_probabilities(state, random.choice(available_actions), eps)
                for a in available_actions:
                    Q[(state, a)] = 0
                    N[(state, a)] = 0
    return policy, Q, N

def select_action_according_to_policy(policy, state):
    return random.choices(list(policy[state].keys()), list(policy[state].values()))[0]

def get_line_grid_intersections(line_start_x, line_start_y, line_end_x, line_end_y):
    row_indices, col_indices = line(line_start_y, line_start_x, line_end_y, line_end_x)
    return [(col_indices[i], row_indices[i]) for i in range(len(row_indices))]

def check_intersections(starting_line, finishing_line, track, intersections):
    for intersection in intersections:
        if intersection not in starting_line.union(track).union(finishing_line):
            return "out_of_bounds"
        if intersection in finishing_line:
            return "finished"
    return "on_track"

def generate_episode(starting_line, finishing_line, track, policy,
    max_num_steps=1000000, noise=0):
    states = []
    actions = []
    rewards = []
    state = generate_start_state(starting_line)
    for t in range(max_num_steps):
        states.append(state)
        x, y, v_x, v_y = state
        action = select_action_according_to_policy(policy, state)
        actions.append(action)
        if random.random() < noise:
            action = (0, 0)
        new_v_x = v_x + action[0]
        new_v_y = v_y + action[1]
        new_x = x + new_v_x
        new_y = y + new_v_y
        state = (new_x, new_y, new_v_x, new_v_y)
        intersections = get_line_grid_intersections(x, y, new_x, new_y)
        intersection_status = check_intersections(
            starting_line, finishing_line, track, intersections
        )
        if intersection_status == "out_of_bounds":
            state = generate_start_state(starting_line)
        elif intersection_status == "finished":
            rewards.append(0)
            break
        rewards.append(-1)
    return states, actions, rewards

def get_greedy_action(Q, state):
    max_val = -np.inf
    greedy_action = None
    for action in get_available_actions(state):
        if Q[(state, action)] > max_val:
            max_val = Q[(state, action)]
            greedy_action = action
    return greedy_action

# On-policy every visit MC control (eps-soft policies)
def learn_from_episode(policy, Q, N, states, actions, rewards, gamma=1, eps=0.1):
    G = 0
    for t in range(len(states) - 1, -1, -1):
        G = gamma * G + rewards[t]
        s = states[t]
        a = actions[t]
        N[(s, a)] += 1
        Q[(s, a)] += (G - Q[(s, a)]) / N[(s, a)]
        policy[s] = get_eps_greedy_probabilities(s, get_greedy_action(Q, s), eps)
    return policy, Q, N

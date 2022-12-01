import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random
from skimage.draw import line

def get_large_map():
    starting_line = {(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)}
    finishing_line = {(16, 26), (16, 27), (16, 28), (16, 29), (16, 30), (16, 31)}
    track = {
        (3,1), (4,1), (5,1), (6,1), (7,1), (8,1),
        (3,2), (4,2), (5,2), (6,2), (7,2), (8,2),
        (2,3), (3,3), (4,3), (5,3), (6,3), (7,3), (8,3),
        (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4),
        (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5),
        (2,6), (3,6), (4,6), (5,6), (6,6), (7,6), (8,6),
        (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (8,7),
        (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8),
        (2,9), (3,9), (4,9), (5,9), (6,9), (7,9), (8,9),
        (1,10), (2,10), (3,10), (4,10), (5,10), (6,10), (7,10), (8,10),
        (1,11), (2,11), (3,11), (4,11), (5,11), (6,11), (7,11), (8,11),
        (1,12), (2,12), (3,12), (4,12), (5,12), (6,12), (7,12), (8,12),
        (1,13), (2,13), (3,13), (4,13), (5,13), (6,13), (7,13), (8,13),
        (1,14), (2,14), (3,14), (4,14), (5,14), (6,14), (7,14), (8,14),
        (1,15), (2,15), (3,15), (4,15), (5,15), (6,15), (7,15), (8,15),
        (1,16), (2,16), (3,16), (4,16), (5,16), (6,16), (7,16), (8,16),
        (1,17), (2,17), (3,17), (4,17), (5,17), (6,17), (7,17), (8,17),
        (0,18), (1,18), (2,18), (3,18), (4,18), (5,18), (6,18), (7,18), (8,18),
        (0,19), (1,19), (2,19), (3,19), (4,19), (5,19), (6,19), (7,19), (8,19),
        (0,20), (1,20), (2,20), (3,20), (4,20), (5,20), (6,20), (7,20), (8,20),
        (0,21), (1,21), (2,21), (3,21), (4,21), (5,21), (6,21), (7,21), (8,21),
        (0,22), (1,22), (2,22), (3,22), (4,22), (5,22), (6,22), (7,22), (8,22),
        (0,23), (1,23), (2,23), (3,23), (4,23), (5,23), (6,23), (7,23), (8,23),
        (0,24), (1,24), (2,24), (3,24), (4,24), (5,24), (6,24), (7,24), (8,24),
        (0,25), (1,25), (2,25), (3,25), (4,25), (5,25), (6,25), (7,25), (8,25), (9,25),
        (0,26), (1,26), (2,26), (3,26), (4,26), (5,26), (6,26), (7,26), (8,26), (9,26), (10,26), (11,26), (12,26), (13,26), (14,26), (15,26),
        (0,27), (1,27), (2,27), (3,27), (4,27), (5,27), (6,27), (7,27), (8,27), (9,27), (10,27), (11,27), (12,27), (13,27), (14,27), (15,27),
        (1,28), (2,28), (3,28), (4,28), (5,28), (6,28), (7,28), (8,28), (9,28), (10,28), (11,28), (12,28), (13,28), (14,28), (15,28),
        (2,29), (3,29), (4,29), (5,29), (6,29), (7,29), (8,29), (9,29), (10,29), (11,29), (12,29), (13,29), (14,29), (15,29),
        (2,30), (3,30), (4,30), (5,30), (6,30), (7,30), (8,30), (9,30), (10,30), (11,30), (12,30), (13,30), (14,30), (15,30),
        (3,31), (4,31), (5,31), (6,31), (7,31), (8,31), (9,31), (10,31), (11,31), (12,31), (13,31), (14,31), (15,31)
    }
    return starting_line, finishing_line, track

def get_medium_map():
    starting_line = {(3, 0), (4, 0), (5, 0), (6, 0)}
    finishing_line = {(9, 3), (9, 4), (9, 5), (9, 6)}
    track = {
        (3,1), (4,1), (5,1), (6,1),
        (3,2), (4,2), (5,2), (6,2),
        (3,3), (4,3), (5,3), (6,3), (7,3), (8,3),
        (3,4), (4,4), (5,4), (6,4), (7,4), (8,4),
        (3,5), (4,5), (5,5), (6,5), (7,5), (8,5),
        (3,6), (4,6), (5,6), (6,6), (7,6), (8,6),
    }
    return starting_line, finishing_line, track

def get_small_map():
    starting_line = {(3, 0)}
    finishing_line = {(4, 2)}
    track = {(3,1), (3,2)}
    return starting_line, finishing_line, track

def get_tiny_map():
    starting_line = {(3, 0)}
    finishing_line = {(4, 1)}
    track = {(3,1)}
    return starting_line, finishing_line, track

def get_super_tiny_map():
    starting_line = {(3, 0)}
    finishing_line = {(4, 0)}
    track = {}
    return starting_line, finishing_line, track

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

def generate_start_state(starting_line):
    start_x, start_y = random.choice(list(starting_line))
    return start_x, start_y, 0, 0

def select_action_according_to_policy(policy, state, eps):
    if random.random() < eps:
        return random.choice(get_available_actions(state))
    return policy[state]

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
    max_num_steps=1000000, noise=0, eps=0):
    states = []
    actions = []
    rewards = []
    state = generate_start_state(starting_line)
    for t in range(max_num_steps):
        states.append(state)
        x, y, v_x, v_y = state
        action = select_action_according_to_policy(policy, state, eps)
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

def initialize_learning_on_pol(starting_line, track):
    policy = {}
    Q = {}
    N = {}
    for x, y in starting_line.union(track):
        for v_x in range(6):
            for v_y in range(6):
                state = (x, y, v_x, v_y)
                available_actions = get_available_actions(state)
                policy[state] = random.choice(available_actions)
                for a in available_actions:
                    Q[(state, a)] = 0
                    N[(state, a)] = 0
    return policy, Q, N

def initialize_learning_off_pol(starting_line, track):
    policy = {}
    b = {}
    Q = {}
    C = {}
    for x, y in starting_line.union(track):
        for v_x in range(6):
            for v_y in range(6):
                state = (x, y, v_x, v_y)
                available_actions = get_available_actions(state)
                policy[state] = available_actions[-1]
                b[state] = policy[state]
                for a in available_actions:
                    Q[(state, a)] = 0
                    C[(state, a)] = 0
    return policy, b, Q, C

# On-policy every visit MC control (eps-soft policies)
def learn_from_episode_on_pol(policy, Q, N, states, actions, rewards, learning_rate=None):
    G = 0
    for t in range(len(states) - 1, -1, -1):
        s = states[t]
        a = actions[t]
        G = G + rewards[t]
        N[(s, a)] += 1
        if learning_rate is not None:
            Q[(s, a)] += learning_rate * (G - Q[(s, a)])
        else:
            Q[(s, a)] += (G - Q[(s, a)]) / N[(s, a)]
        policy[s] = get_greedy_action(Q, s)
    return policy, Q, N

# Off-policy every visit MC control (weighted importance sampling)
def learn_from_episode_off_pol(policy, b, Q, C, states, actions, rewards):
    G = 0
    W = 1
    for t in range(len(states) - 1, -1, -1):
        s = states[t]
        a = actions[t]
        G = G + rewards[t]
        C[(s, a)] += W
        Q[(s, a)] += (W / C[(s, a)]) * (G - Q[(s, a)])
        
        # Argmax over a, break ties by favoring the last selected action by b,
        # then by the deterministic ordering of get_greedy_action.
        # If not "favoring the last selected action by b", and simply relying on
        # the ordering of get_greedy_action, the algorithm can easily get stuck,
        # even though get_greedy_action provides consistent ordering.
        #greedy_action = get_greedy_action(Q, s)
        #if Q[(s, a)] == Q[(s, greedy_action)]:
        #    policy[s] = a
        #else:
        #    policy[s] = greedy_action
        policy[s] = get_greedy_action(Q, s)
        b[s] = policy[s]

        if policy[s] != a:
            break
        W = W * (1 / b[s][a])
    return policy, b, Q, C

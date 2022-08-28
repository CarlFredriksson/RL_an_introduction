import numpy as np
from scipy.special import iv
import matplotlib.pyplot as plt
import seaborn as sns

# Probability mass function for Poisson distribution p(K=k)
def poisson_pmf(lam, k):
    return (np.power(lam, k) / np.math.factorial(k)) * np.exp(-lam)

# Cumulative distribution function for Poisson distribution p(K<=k)
def poisson_cdf(lam, k):
    return np.sum([poisson_pmf(lam, n) for n in range(k + 1)])

# Probability mass function for Skellam distribution p(K=k)
def skellam_pmf(mu_1, mu_2, k):
    return np.exp(-(mu_1 + mu_2)) * np.power(mu_1 / mu_2, k/2) * iv(np.abs(k), 2 * np.sqrt(mu_1 * mu_2))

# r(s, a)
def expected_immediate_reward(state, action, expected_num_req, reward_per_rented_car=10, cost_per_moved_car=2):
    # Expected reward for location 1
    expected_reward_loc1 = 0
    for i in range(state[0]):
        expected_reward_loc1 += reward_per_rented_car * i * poisson_pmf(expected_num_req[0], i)
    expected_reward_loc1 += reward_per_rented_car * state[0] * (1 - poisson_cdf(expected_num_req[0], state[0] - 1))

    # Expected reward for location 2
    expected_reward_loc2 = 0
    for i in range(state[1]):
        expected_reward_loc2 += reward_per_rented_car * i * poisson_pmf(expected_num_req[1], i)
    expected_reward_loc2 += reward_per_rented_car * state[1] * (1 - poisson_cdf(expected_num_req[1], state[1] - 1))

    movement_cost = np.abs(action) * cost_per_moved_car

    return expected_reward_loc1 + expected_reward_loc2 - movement_cost

"""
# p(s' | s, a)
# NOTE: Edge cases for next state values 0 and 20 are not handled perfectly according to
# the problem statement, since returns that lead to >20 and requests that lead to <0 aren't counted.
def transition_probability(next_state, state, action, expected_num_req, expected_num_ret):
    # Trying to move cars that aren't there
    if action > state[0] or -action > state[1]:
        return 0
    
    # Move cars
    num_cars = (state[0] - action, state[1] + action)

    # Probability for num_cars[0] to get to next_state[0] after requests and returns
    diff = next_state[0] - num_cars[0]
    prob_1 = skellam_pmf(expected_num_ret[0], expected_num_req[0], diff)

    # Probability for num_cars[1] to get to next_state[1] after requests and returns
    diff = next_state[1] - num_cars[1]
    prob_2 = skellam_pmf(expected_num_ret[1], expected_num_req[1], diff)

    return prob_1 * prob_2
"""

# p(s' | s, a)
# NOTE: Edge cases for next state values 0 and 20 are not handled perfectly according to
# the problem statement, since returns that lead to >20 and requests that lead to <0 aren't counted.
def transition_probability(next_state, state, action, expected_num_req, expected_num_ret):
    # Trying to move cars that aren't there
    if action > state[0] or -action > state[1]:
        return 0
    
    # Move cars
    num_cars = (state[0] - action, state[1] + action)

    # Probability for num_cars[0] to get to next_state[0] after requests and returns
    diff = next_state[0] - num_cars[0]
    prob_1 = skellam_pmf(expected_num_ret[0], expected_num_req[0], diff)

    if next_state[0] == 0:
        prob_1 = 0
        for i in range()
    #elif next_state[0] == 20:

    # Probability for num_cars[1] to get to next_state[1] after requests and returns
    diff = next_state[1] - num_cars[1]
    prob_2 = skellam_pmf(expected_num_ret[1], expected_num_req[1], diff)

    return prob_1 * prob_2

def update_state_value(state_values, state, action, expected_num_req, expected_num_ret, discount_rate):
    new_state_value = expected_immediate_reward(state, action, expected_num_req)
    for i in range(state_values.shape[0]):
        for j in range(state_values.shape[1]):
            next_state = (i, j)
            new_state_value += (
                discount_rate
                * transition_probability(next_state, state, action, expected_num_req, expected_num_ret)
                * state_values[i ,j]
            )
    return new_state_value

def policy_evaluation(init_state_values, deterministic_policy, expected_num_req, expected_num_ret,
                      discount_rate, max_num_iterations, policy_eval_threshold):
    state_values = init_state_values.copy()
    for i in range(max_num_iterations):
        delta = 0
        for j in range(state_values.shape[0]):
            for k in range(state_values.shape[1]):
                state = (j, k)
                action = deterministic_policy[j, k]
                old_state_value = state_values[j, k]
                state_values[j, k] = update_state_value(
                    state_values, state, action, expected_num_req, expected_num_ret, discount_rate
                )
            delta = np.max((delta, np.abs(old_state_value - state_values[j, k])))
        if delta < policy_eval_threshold:
            break
    print("num eval iterations:", i)
    return state_values

def find_maximizing_action(state_values, state, expected_num_req, expected_num_ret, discount_rate, max_num_moves):
    maximizing_action = 0
    max_state_action_value = -np.inf
    possible_actions = range(-np.min((state[1], max_num_moves)), np.min((state[0], max_num_moves)) + 1)
    for action in possible_actions:
        state_action_value = expected_immediate_reward(state, action, expected_num_req)
        for i in range(state_values.shape[0]):
            for j in range(state_values.shape[1]):
                next_state = (i, j)
                state_action_value += (
                    discount_rate
                    * transition_probability(next_state, state, action, expected_num_req, expected_num_ret)
                    * state_values[i ,j]
                )
        if state_action_value > max_state_action_value:
            maximizing_action = action
            max_state_action_value = state_action_value
    return maximizing_action, max_state_action_value

def policy_improvement(state_values, init_deterministic_policy, expected_num_req, expected_num_ret,
                       discount_rate, max_num_moves, policy_eval_threshold):
    deterministic_policy = init_deterministic_policy.copy()
    policy_stable = True
    for i in range(state_values.shape[0]):
        for j in range(state_values.shape[1]):
            state = (i, j)
            maximizing_action, max_state_action_value = find_maximizing_action(state_values, state,
                expected_num_req, expected_num_ret, discount_rate, max_num_moves)
            deterministic_policy[i, j] = maximizing_action
            if max_state_action_value > state_values[i, j] + policy_eval_threshold:
                policy_stable = False
    return deterministic_policy, policy_stable

def plot_deterministic_policy(deterministic_policy):
    plt.figure(figsize = (8, 6))
    ax = sns.heatmap(deterministic_policy, linewidth=0.5, vmin=-5, vmax=5, annot=True)
    ax.invert_yaxis()
    plt.show()

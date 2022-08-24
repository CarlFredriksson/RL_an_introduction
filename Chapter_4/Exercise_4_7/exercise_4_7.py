import numpy as np
from scipy.special import factorial

# Probability mass function for poisson distribution p(X=x)
def poisson_pmf(lam, x):
    return (np.power(lam, x) / factorial(x)) * np.exp(-lam)

# Cumulative distribution function for poisson distribution p(X<=x)
def poisson_cdf(lam, x):
    return np.sum([poisson_pmf(lam, n) for n in range(x + 1)])

# r(s, a)
def expected_immediate_reward(state, action, expected_num_req_loc1, expected_num_req_loc2,
                              reward_per_rented_car=10, cost_per_moved_car=2):
    expected_reward_loc1 = 0
    for i in range(state[0]):
        expected_reward_loc1 += reward_per_rented_car * i * poisson_pmf(expected_num_req_loc1, i)
    expected_reward_loc1 += reward_per_rented_car * state[0] * (1 - poisson_cdf(expected_num_req_loc1, state[0] - 1))

    expected_reward_loc2 = 0
    for i in range(state[1]):
        expected_reward_loc2 += reward_per_rented_car * i * poisson_pmf(expected_num_req_loc2, i)
    expected_reward_loc2 += reward_per_rented_car * state[1] * (1 - poisson_cdf(expected_num_req_loc2, state[1] - 1))

    movement_cost = np.abs(action) * cost_per_moved_car

    return expected_reward_loc1 + expected_reward_loc2 - movement_cost

# p(s', r | s, a)
def dynamics_function(new_state, reward, old_state, action):
    # Trying to move cars that aren't there
    if action > old_state[0] or -action > old_state[1]:
        return 0
    # TODO: Change to p(s' | s, a) and r(s, a) instead?

    return 0

def update_state_value(state_values, state, action, rewards, discount_rate):
    new_state_value = 0
    for i in range(21):
        for j in range(21):
            next_state = (i, j)
            for r in rewards:
                new_state_value += dynamics_function(next_state, r, state, action) * (r + discount_rate * state_values[i, j])
    return new_state_value

def policy_evaluation(init_state_values, init_deterministic_policy, rewards, discount_rate=0.9,
                      max_num_iterations=1000, policy_evaluation_threshold=0.01):
    state_values = init_state_values.copy()
    deterministic_policy = init_deterministic_policy.copy()
    for i in range(max_num_iterations):
        delta = 0
        for j in range(state_values.shape[0]):
            for k in range(state_values.shape[1]):
                state = (j, k)
                action = deterministic_policy[j, k]
                old_state_value = state_values[j, k]
                state_values[j, k] = update_state_value(state_values, state, action, rewards, discount_rate)
            delta = np.max((delta, np.abs(old_state_value - state_values[j, k])))
        if delta < policy_evaluation_threshold:
            break
    return state_values, deterministic_policy

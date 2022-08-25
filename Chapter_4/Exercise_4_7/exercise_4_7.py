import numpy as np

# Probability mass function for poisson distribution p(X=x)
def poisson_pmf(lam, x):
    return (np.power(lam, x) / np.math.factorial(x)) * np.exp(-lam)

# Cumulative distribution function for poisson distribution p(X<=x)
def poisson_cdf(lam, x):
    return np.sum([poisson_pmf(lam, n) for n in range(x + 1)])

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

# p(s' | s, a)
def transition_probability(next_state, state, action, expected_num_req, expected_num_ret, precision=10):
    # Trying to move cars that aren't there
    if action > state[0] or -action > state[1]:
        return 0
    
    # Probability for location 1
    probability_loc1 = 0
    num_cars_to_add = next_state[0] - state[0] + action
    if num_cars_to_add >= 0:
        for num_ret in range(num_cars_to_add, precision + 1):
            num_req = num_ret - num_cars_to_add
            probability_loc1 += poisson_pmf(expected_num_ret[0], num_ret) * poisson_pmf(expected_num_req[0], num_req)
    else:
        for num_req in range(-num_cars_to_add, precision + 1):
            num_ret = num_req + num_cars_to_add
            probability_loc1 += poisson_pmf(expected_num_ret[0], num_ret) * poisson_pmf(expected_num_req[0], num_req)
    
    # Probability for location 2
    probability_loc2 = 0
    num_cars_to_add = next_state[1] - state[1] - action
    if num_cars_to_add >= 0:
        for num_ret in range(num_cars_to_add, precision + 1):
            num_req = num_ret - num_cars_to_add
            probability_loc2 += poisson_pmf(expected_num_ret[1], num_ret) * poisson_pmf(expected_num_req[1], num_req)
    else:
        for num_req in range(-num_cars_to_add, precision + 1):
            num_ret = num_req + num_cars_to_add
            probability_loc2 += poisson_pmf(expected_num_ret[1], num_ret) * poisson_pmf(expected_num_req[1], num_req)

    return probability_loc1 * probability_loc2

def update_state_value(state_values, state, action, expected_num_req, expected_num_ret, discount_rate):
    new_state_value = expected_immediate_reward(state, action, expected_num_req)
    for i in range(21):
        for j in range(21):
            next_state = (i, j)
            new_state_value += (
                discount_rate
                * transition_probability(next_state, state, action, expected_num_req, expected_num_ret)
                * state_values[i ,j]
            )
    return new_state_value

def policy_evaluation(init_state_values, init_deterministic_policy, expected_num_req=(3, 4), expected_num_ret=(3, 2),
                      discount_rate=0.9, max_num_iterations=1000, policy_evaluation_threshold=0.01):
    state_values = init_state_values.copy()
    deterministic_policy = init_deterministic_policy.copy()
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
        if delta < policy_evaluation_threshold:
            break
    return state_values, deterministic_policy

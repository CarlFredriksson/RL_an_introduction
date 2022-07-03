import numpy as np
rng = np.random.default_rng()

def argmax_random_tiebreak(x):
    return rng.choice(np.flatnonzero(x == x.max()))

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x))

def epsilon_greedy_selection(action_value_estimates, exploration_probability):
    if rng.random() < exploration_probability:
        return rng.integers(0, len(action_value_estimates))
    return argmax_random_tiebreak(action_value_estimates)

def ucb_selection(time_step, action_value_estimates, num_action_selections, uncertainty_constant):
    unselected_actions = np.flatnonzero(num_action_selections == 0)
    if len(unselected_actions) > 0:
        return rng.choice(unselected_actions)
    upper_confidence_bounds = action_value_estimates + uncertainty_constant * np.sqrt(np.log(time_step) / num_action_selections)
    return argmax_random_tiebreak(upper_confidence_bounds)

def softmax_selection(action_preferences):
    return rng.choice(len(action_preferences), p=softmax(action_preferences))

def compute_reward(action_values, selected_action):
    reward = rng.normal(action_values[selected_action], 1)
    selected_optimal_action = action_values[selected_action] == action_values.max()
    return reward, selected_optimal_action

def update_action_value_estimates(action_value_estimates, num_action_selections, selected_action, reward, constant_step_size=None):
    step_size = 1 / num_action_selections[selected_action]
    if constant_step_size is not None:
        step_size = constant_step_size
    estimates = action_value_estimates.copy()
    estimates[selected_action] += step_size * (reward - estimates[selected_action])
    return estimates

def update_action_preferences(action_preferences, selected_action, reward, prev_rewards_avg, constant_step_size):
    selection_probabilities = softmax(action_preferences)
    preferences = action_preferences - constant_step_size * (reward - prev_rewards_avg) * selection_probabilities
    preferences[selected_action] = (action_preferences[selected_action] +
        constant_step_size * (reward - prev_rewards_avg) * (1 - selection_probabilities[selected_action]))
    return preferences
 
def run_action_value_method(num_steps, num_actions, stationary, exploration_probability, initial_action_value_estimate,
                            constant_step_size=None, uncertainty_constant=None):
    # Initialize
    rewards = np.zeros(num_steps)
    optimal_action_selections = np.zeros(num_steps)
    action_values = rng.standard_normal(num_actions)
    if not stationary:
        action_values = np.ones(num_actions) * rng.standard_normal()
    action_value_estimates = np.ones(num_actions) * initial_action_value_estimate
    num_action_selections = np.zeros(num_actions)

    # Run simulation
    for i in range(num_steps):
        if not stationary:
            action_values += rng.normal(0, 0.01, num_actions)
        selected_action = -1
        if uncertainty_constant is None:
            selected_action = epsilon_greedy_selection(action_value_estimates, exploration_probability)
        else:
            selected_action = ucb_selection(i + 1, action_value_estimates, num_action_selections, uncertainty_constant)
        num_action_selections[selected_action] += 1
        reward, selected_optimal_action = compute_reward(action_values, selected_action)
        rewards[i] = reward
        if selected_optimal_action:
            optimal_action_selections[i] = 1
        action_value_estimates = update_action_value_estimates(
            action_value_estimates, num_action_selections, selected_action, reward, constant_step_size)
    
    return rewards, optimal_action_selections

def run_multiple_action_value_methods(num_simulations, num_steps, num_actions, stationary, exploration_probability, initial_action_value_estimate,
                                      constant_step_size=None, uncertainty_constant=None):
    average_rewards = np.zeros(num_steps)
    optimal_action_proportions = np.zeros(num_steps)
    for i in range(num_simulations):
        rewards, optimal_action_selections = run_action_value_method(num_steps, num_actions, stationary, exploration_probability,
            initial_action_value_estimate, constant_step_size, uncertainty_constant)
        average_rewards += rewards
        optimal_action_proportions += optimal_action_selections
    average_rewards /= num_simulations
    optimal_action_proportions /= num_simulations
    return average_rewards, optimal_action_proportions

def run_gradient_method(num_steps, num_actions, stationary, constant_step_size):
    # Initialize
    rewards = np.zeros(num_steps)
    optimal_action_selections = np.zeros(num_steps)
    action_values = rng.standard_normal(num_actions)
    if not stationary:
        action_values = np.ones(num_actions) * rng.standard_normal()
    action_preferences = np.zeros(num_actions)

    # Run simulation
    for i in range(num_steps):
        if not stationary:
            action_values += rng.normal(0, 0.01, num_actions)
        prev_rewards_avg = np.average(rewards)
        selected_action = softmax_selection(action_preferences)
        reward, selected_optimal_action = compute_reward(action_values, selected_action)
        rewards[i] = reward
        if selected_optimal_action:
            optimal_action_selections[i] = 1
        action_preferences = update_action_preferences(action_preferences, selected_action, reward, prev_rewards_avg, constant_step_size)
    
    return rewards, optimal_action_selections

def run_multiple_gradient_methods(num_simulations, num_steps, num_actions, stationary, constant_step_size):
    average_rewards = np.zeros(num_steps)
    optimal_action_proportions = np.zeros(num_steps)
    for i in range(num_simulations):
        rewards, optimal_action_selections = run_gradient_method(num_steps, num_actions, stationary, constant_step_size)
        average_rewards += rewards
        optimal_action_proportions += optimal_action_selections
    average_rewards /= num_simulations
    optimal_action_proportions /= num_simulations
    return average_rewards, optimal_action_proportions

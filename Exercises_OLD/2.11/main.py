import numpy as np
import matplotlib.pyplot as plt
import math

def my_argmax(Q_values):
    """
    Returns the index of the maximum value in Q_values.
    In case of ties, one of the tying indices are selected at uniform-random and returned.
    """
    max_val = -math.inf
    ties = []
    for i in range(len(Q_values)):
        Q_val = Q_values[i]
        if Q_val > max_val:
            max_val = Q_val
            ties = [i]
        elif Q_val == max_val:
            ties.append(i)

    return np.random.choice(ties)

def epsilon_greedy(num_runs, num_steps_per_run, eps, Q_0, const_alpha=None, stationary=True):
    print("Epsilon greedy: Running", num_runs, "runs of", num_steps_per_run, "steps each")
    
    R_avg = np.zeros((num_steps_per_run, 1))
    O_avg = np.zeros((num_steps_per_run, 1))
    
    # Run runs
    for j in range(0, num_runs):
        if j % 100 == 0:
            print("Starting run", j)

        # Init bandit values
        q = np.random.normal(loc=0, scale=1, size=(10, 1))
        if not stationary:
            q = np.ones((10, 1)) * np.random.normal()
        
        # Init value estimation
        Q = np.ones(np.shape(q)) * Q_0
        N = np.zeros(np.shape(q))

        # Run steps
        for i in range(0, num_steps_per_run):
            if not stationary:
                q = q + np.random.normal(scale=0.01, size=np.shape(q))

            # Choose action greedily by default and randomly by probability eps
            a = my_argmax(Q)
            if np.random.uniform(low=0.0, high=1.0) < eps:
                a = np.random.randint(low=0, high=np.shape(Q)[0] - 1)
            N[a] = N[a] + 1
            if a == np.argmax(q):
                O_avg[i] = O_avg[i] + 1 / num_runs

            # Get reward
            R = np.random.normal(loc=q[a])
            R_avg[i] = R_avg[i] + R / num_runs

            # Update Q
            alpha = const_alpha
            if const_alpha is None:
                alpha = (1 / N[a])
            Q[a] = Q[a] + alpha * (R - Q[a])

    return R_avg, O_avg

def ucb(num_runs, num_steps_per_run, c, Q_0, const_alpha=None, stationary=True):
    print("UCB: Running", num_runs, "runs of", num_steps_per_run, "steps each")
    
    R_avg = np.zeros((num_steps_per_run, 1))
    O_avg = np.zeros((num_steps_per_run, 1))
    
    # Run runs
    for j in range(0, num_runs):
        if j % 100 == 0:
            print("Starting run", j)

        # Init bandit values
        q = np.random.normal(loc=0, scale=1, size=(10, 1))
        if not stationary:
            q = np.ones((10, 1)) * np.random.normal()
        
        # Init value estimation
        Q = np.ones(np.shape(q)) * Q_0
        N = np.zeros(np.shape(q))

        # Run steps
        for i in range(0, num_steps_per_run):
            if not stationary:
                q = q + np.random.normal(scale=0.01, size=np.shape(q))

            # Choose action according to the maximum upper-confidence-bound
            ucb_max = -math.inf
            a = -1
            for action in range(0, len(q)):
                if N[action] == 0:
                    a = action
                    break
                ucb_action = Q[action] + c * np.sqrt(np.log(i + 1) / N[action])
                if ucb_action > ucb_max:
                    ucb_max = ucb_action
                    a = action
            N[a] = N[a] + 1
            if a == np.argmax(q):
                O_avg[i] = O_avg[i] + 1 / num_runs

            # Get reward
            R = np.random.normal(loc=q[a])
            R_avg[i] = R_avg[i] + R / num_runs

            # Update Q
            alpha = const_alpha
            if const_alpha is None:
                alpha = (1 / N[a])
            Q[a] = Q[a] + alpha * (R - Q[a])

    return R_avg, O_avg

def gradient_bandit(num_runs, num_steps_per_run, const_alpha=None, stationary=True):
    print("Gradient bandit: Running", num_runs, "runs of", num_steps_per_run, "steps each")

    R_avg = np.zeros((num_steps_per_run, 1))
    O_avg = np.zeros((num_steps_per_run, 1))
    
    # Run runs
    for j in range(0, num_runs):
        if j % 100 == 0:
            print("Starting run", j)

        # Init bandit values
        q = np.random.normal(loc=0, scale=1, size=(10, 1))
        if not stationary:
            q = np.ones((10, 1)) * np.random.normal()
        
        # Init action preferences
        H = np.zeros(np.shape(q))
        N = np.zeros(np.shape(q))

        R_avg_steps = 0

        # Run steps
        for i in range(0, num_steps_per_run):
            if not stationary:
                q = q + np.random.normal(scale=0.01, size=np.shape(q))

            # Choose action by softmax probability distribution over action preferences
            p = np.exp(H) / np.sum(np.exp(H))
            a = np.random.choice(len(q), p=np.reshape(p, (len(p), )))
            N[a] = N[a] + 1
            if a == np.argmax(q):
                O_avg[i] = O_avg[i] + 1 / num_runs

            # Get reward
            R = np.random.normal(loc=q[a])
            R_avg[i] = R_avg[i] + R / num_runs

            # Update R_avg_steps
            alpha = const_alpha
            if const_alpha is None:
                alpha = (1 / N[a])
            R_avg_steps = R_avg_steps + alpha * (R - R_avg_steps)

            # Update H
            for action in range(0, len(q)):
                if action == a:
                    H[action] = H[action] + alpha * (R - R_avg_steps) * (1 - p[action])
                else:
                    H[action] = H[action] - alpha * (R - R_avg_steps) * p[action]

    return R_avg, O_avg

NUM_RUNS = 100
NUM_STEPS_PER_RUN = 1000
CONST_ALPHA = 0.1

epsilon_greedy_results = [
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 1/128, 0, const_alpha=CONST_ALPHA)[0]),
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 1/64, 0, const_alpha=CONST_ALPHA)[0]),
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 1/32, 0, const_alpha=CONST_ALPHA)[0]),
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 1/16, 0, const_alpha=CONST_ALPHA)[0]),
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 1/8, 0, const_alpha=CONST_ALPHA)[0]),
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 1/4, 0, const_alpha=CONST_ALPHA)[0])
]

greedy_results = [
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 0, 1/4, const_alpha=CONST_ALPHA)[0]),
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 0, 1/2, const_alpha=CONST_ALPHA)[0]),
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 0, 1, const_alpha=CONST_ALPHA)[0]),
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 0, 2, const_alpha=CONST_ALPHA)[0]),
    np.mean(epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 0, 4, const_alpha=CONST_ALPHA)[0])
]

ucb_results = [
    np.mean(ucb(NUM_RUNS, NUM_STEPS_PER_RUN, 1/16, 0, const_alpha=CONST_ALPHA)),
    np.mean(ucb(NUM_RUNS, NUM_STEPS_PER_RUN, 1/8, 0, const_alpha=CONST_ALPHA)),
    np.mean(ucb(NUM_RUNS, NUM_STEPS_PER_RUN, 1/4, 0, const_alpha=CONST_ALPHA)),
    np.mean(ucb(NUM_RUNS, NUM_STEPS_PER_RUN, 1/2, 0, const_alpha=CONST_ALPHA)),
    np.mean(ucb(NUM_RUNS, NUM_STEPS_PER_RUN, 1, 0, const_alpha=CONST_ALPHA)),
    np.mean(ucb(NUM_RUNS, NUM_STEPS_PER_RUN, 2, 0, const_alpha=CONST_ALPHA)),
    np.mean(ucb(NUM_RUNS, NUM_STEPS_PER_RUN, 4, 0, const_alpha=CONST_ALPHA)),
]

gradient_bandit_results = [
    np.mean(gradient_bandit(NUM_RUNS, NUM_STEPS_PER_RUN, const_alpha=1/32)[0]),
    np.mean(gradient_bandit(NUM_RUNS, NUM_STEPS_PER_RUN, const_alpha=1/16)[0]),
    np.mean(gradient_bandit(NUM_RUNS, NUM_STEPS_PER_RUN, const_alpha=1/8)[0]),
    np.mean(gradient_bandit(NUM_RUNS, NUM_STEPS_PER_RUN, const_alpha=1/4)[0]),
    np.mean(gradient_bandit(NUM_RUNS, NUM_STEPS_PER_RUN, const_alpha=1/2)[0]),
    np.mean(gradient_bandit(NUM_RUNS, NUM_STEPS_PER_RUN, const_alpha=1)[0]),
    np.mean(gradient_bandit(NUM_RUNS, NUM_STEPS_PER_RUN, const_alpha=2)[0]),
]

plt.plot(np.array([1/128, 1/64, 1/32, 1/16, 1/8, 1/4]), epsilon_greedy_results, label="Epsilon greedy")
plt.plot(np.array([1/4, 1/2, 1, 2, 4]), greedy_results, label="Greedy")
plt.plot(np.array([1/16, 1/8, 1/4, 1/2, 1, 2, 4]), ucb_results, label="UCB")
plt.plot(np.array([1/32, 1/16, 1/8, 1/4, 1/2, 1, 2]), ucb_results, label="Gradient bandit")
plt.xlabel("Parameter setting")
plt.ylabel("Average reward")
plt.xscale("log")
plt.xticks([1/128, 1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1, 2, 4], ["1/128", "1/64", "1/32", "1/16", "1/8", "1/4", "1/2", "1", "2", "4"])
plt.legend(bbox_to_anchor=(1.04, 1))
plt.tight_layout()
plt.savefig("results.png")

"""
Results = [
    epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 0.1, 0, const_alpha=CONST_ALPHA),
    epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, 0, 2, const_alpha=CONST_ALPHA),
    ucb(NUM_RUNS, NUM_STEPS_PER_RUN, 1, 0, const_alpha=CONST_ALPHA),
    gradient_bandit(NUM_RUNS, NUM_STEPS_PER_RUN, const_alpha=CONST_ALPHA)
]

# Plot results
plt.subplot(2, 1, 1)
x = np.arange(0, NUM_STEPS_PER_RUN)
plt.plot(x, Results[0][0], label="Epsilon greedy, eps=0.1, Q_0=0, alpha=" + str(CONST_ALPHA))
plt.plot(x, Results[1][0], label="Epsilon greedy, eps=0, Q_0=2, alpha=" + str(CONST_ALPHA))
plt.plot(x, Results[2][0], label="UCB, c=1, Q_0=0, alpha=" + str(CONST_ALPHA))
plt.plot(x, Results[3][0], label="Gradient bandit, alpha=" + str(CONST_ALPHA))
plt.legend(bbox_to_anchor=(1.04, 1))
plt.xlabel("Step")
plt.ylabel("Average reward")
plt.title("Stationary")
plt.subplot(2, 1, 2)
plt.plot(x, Results[0][1], label="Epsilon greedy, eps=0.1, Q_0=0, alpha=" + str(CONST_ALPHA))
plt.plot(x, Results[1][1], label="Epsilon greedy, eps=0, Q_0=2, alpha=" + str(CONST_ALPHA))
plt.plot(x, Results[2][1], label="UCB, c=2, Q_0=0, alpha=" + str(CONST_ALPHA))
plt.plot(x, Results[3][1], label="Gradient bandit, alpha=" + str(CONST_ALPHA))
plt.xlabel("Step")
plt.ylabel("Fraction optimal action")
plt.legend(bbox_to_anchor=(1.04, 1))
plt.tight_layout()
plt.savefig("results.png")
"""

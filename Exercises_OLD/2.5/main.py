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

def epsilon_greedy(num_runs, num_steps_per_run, eps, const_alpha=None, stationary=True):
    print("Running", num_runs, "runs of", num_steps_per_run, "steps each")
    
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
        Q = np.zeros(np.shape(q))
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

NUM_RUNS = 1000
NUM_STEPS_PER_RUN = 1000
EPS = 0.1
CONST_ALPHA = 0.1
R_avg_sample, O_avg_sample = epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, EPS)
R_avg_alpha, O_avg_alpha = epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, EPS, const_alpha=CONST_ALPHA)
R_avg_sample_non_stationary, O_avg_sample_non_stationary = epsilon_greedy(NUM_RUNS, NUM_STEPS_PER_RUN, EPS, stationary=False)
R_avg_alpha_non_stationary, O_avg_alpha_non_stationary = epsilon_greedy(NUM_RUNS,
    NUM_STEPS_PER_RUN, EPS, const_alpha=CONST_ALPHA, stationary=False)

# Plot results
plt.subplot(2, 1, 1)
x = np.arange(0, NUM_STEPS_PER_RUN)
plt.plot(x, R_avg_sample, label="Stationary, alpha=1/N(A)")
plt.plot(x, R_avg_alpha, label="Stationary, alpha=" + str(CONST_ALPHA))
plt.plot(x, R_avg_sample_non_stationary, label="Non-stationary, alpha=1/N(A)")
plt.plot(x, R_avg_alpha_non_stationary, label="Non-stationary, alpha=" + str(CONST_ALPHA))
plt.legend(bbox_to_anchor=(1.04, 1))
plt.xlabel("Step")
plt.ylabel("Average reward")
plt.subplot(2, 1, 2)
plt.plot(x, O_avg_sample, label="Stationary, alpha=1/N(A)")
plt.plot(x, O_avg_alpha, label="Stationary, alpha=" + str(CONST_ALPHA))
plt.plot(x, O_avg_sample_non_stationary, label="Non-stationary, alpha=1/N(A)")
plt.plot(x, O_avg_alpha_non_stationary, label="Non-stationary, alpha=" + str(CONST_ALPHA))
plt.xlabel("Step")
plt.ylabel("Fraction optimal action")
plt.legend(bbox_to_anchor=(1.04, 1))
plt.tight_layout()
plt.savefig("results.png")

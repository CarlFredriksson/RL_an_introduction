import numpy as np

def poission(lam, n):
    return lam**n / np.math.factorial(n) * np.exp(-lam)

def p(s_prime, r, s, a):
    p_sum = 0

    for r_0 in range(r + 1):
        r_1 = r - r_0
        b_0 = s_prime[0] - s[0] + r_0 - a
        b_1 = s_prime[1] - s[1] + r_1 + a
        if b_0 >= 0 and b_1 >= 0:
            p_sum += poission(3, r_0) * poission(4, r_1) * poission(3, b_0) * poission(2, b_1)

    return p_sum

def compute_new_V(V, s, pi, discount_rate=0.9):
    v = 0

    for s_prime_0 in range(21):
        for s_prime_1 in range(21):
            s_prime = (s_prime_0, s_prime_1)
            for r in range(21):
                v += p(s_prime, r, s, pi[s]) * (r + discount_rate * V[s_prime])

    return v

def policy_eval(V, pi, eps = 0.1, max_num_iterations = 10):
    for i in range(0, max_num_iterations):
        print("i:", i)
        delta = 0
        for s_0 in range(21):
            for s_1 in range(21):
                s = (s_0, s_1)
                print("s:", s)
                v_old = V[s]
                V[s] = compute_new_V(V, s, pi)
                delta = np.max((delta, np.abs(V[s] - v_old)))
        if delta < eps:
            break
    return V

pi = np.zeros((21, 21))
V = np.zeros((21, 21))

print(policy_eval(V, pi))

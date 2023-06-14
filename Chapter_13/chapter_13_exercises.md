# Exercises - Chapter 13

Carl Fredriksson, c@msp.se

## Exercise 13.1

Use your knowledge of the gridworld and its dynamics to determine an exact symbolic expression for the optimal probability of selecting the **right** action in Example 13.1.

**My answer:**

Let $A$ denote the second state and $B$ the third state ($S$ is the starting state). We can use the Bellman equation for state values

$$
v_\pi(s) = \sum_{a} \pi(a|s) \sum_{s^\prime,r} p(s^\prime, r|s,a) \big[r + \gamma v_\pi(s^\prime)\big] \text{,} \quad \text{for all} \quad s\in\mathcal{S}
$$

to set up a system of equations

$$
\begin{cases}
v_\pi(S) = \pi(right) \big[-1 + v_\pi(A)\big] + \pi(left) \big[-1 + v_\pi(S)\big] \\
v_\pi(A) = \pi(right) \big[-1 + v_\pi(S)\big] + \pi(left) \big[-1 + v_\pi(B)\big] \\
v_\pi(S) = \pi(right) \big[-1\big] + \pi(left) \big[-1 + v_\pi(A)\big]
\end{cases}
$$

Let $p=\pi(right)$ and note that $\pi(left) = 1-p$, we can rewrite the equations as

$$
\begin{cases}
v_\pi(S) = p \big[-1 + v_\pi(A)\big] + (1-p) \big[-1 + v_\pi(S)\big] \\
v_\pi(A) = p\big[-1 + v_\pi(S)\big] + (1-p) \big[-1 + v_\pi(B)\big] \\
v_\pi(S) = p \big[-1\big] + (1-p) \big[-1 + v_\pi(A)\big]
\end{cases}
$$

$$
\begin{cases}
v_\pi(S) = -1 + p v_\pi(A) + (1-p) v_\pi(S) \\
v_\pi(A) = -1 + p v_\pi(S) + (1-p) v_\pi(B) \\
v_\pi(S) = -1 + (1-p) v_\pi(A)
\end{cases}
$$

The system can be solved to get

$$
v_\pi(S) = -2 \frac{2-p}{p(1-p)}
$$

Our goal is to compute $\max{\{v_\pi(S) \; | \;0<p<1\}}$ ($p$ is a probability and both $p=0$ and $p=1$ means that the agent will never get to the goal state from the starting state). First we find all critical points, i.e. where the derivative is either zero or doesn't exist.

$$
\frac{\delta v_\pi(S)}{\delta p} = -2 \frac{p(1-p)(-1) - (2-p)(1-2p)}{p^2(1-p)^2}
$$

The derivative doesn't exist for $p=0$ or $p=1$, but since neither critical point satisfies $0<p<1$, we can disregard them. That leaves us with the points where the derivative is zero.

$$
\frac{\delta v_\pi(S)}{\delta p} = 0 \implies p(1-p)(-1) = (2-p)(1-2p)
$$

This equation can be solved to get

$$
p = 2 \plusmn \sqrt{2}
$$

Only $p=2-\sqrt{2} \approx 0.5858$ satisfies $0<p<1$, which means that we have found our optimal probability $p$ of selecting the **right** action. We can use this probability to check that we get the same value for the start state as given in example 13.1

$$
v_\pi(S) = -2 \frac{2-p}{p(1-p)} = -2 \frac{2-(2-\sqrt{2})}{(2-\sqrt{2})(1-(2-\sqrt{2}))} = -6 - 4 \sqrt{2} \approx 11.66
$$

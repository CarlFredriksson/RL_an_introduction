# Exercises - Chapter 4

Carl Fredriksson, c@msp.se

## Exercise 4.1

In Example 4.1, if $\pi$ is the equiprobable random policy, what is $q_\pi(11, down)$? What is $q_\pi(7, down)$?

**My answer:**

$$
\begin{aligned}
q_\pi(11, down) &= \sum_{s^\prime, r} p(s^\prime, r | 11, down) \big[r + v_\pi(s^\prime) \big] \\
&= -1 + v_\pi(terminal) \\
&= -1
\end{aligned}
$$

$$
\begin{aligned}
q_\pi(7, down) &= \sum_{s^\prime, r} p(s^\prime, r | 7, down) \big[r + v_\pi(s^\prime) \big] \\
&= -1 + v_\pi(11) \\
&= -15
\end{aligned}
$$

The values for $v_\pi$ can be seen in figure 4.1.

## Exercise 4.2

In Example 4.1, suppose a new state 15 is added to the gridworld just below state 13, and its actions, left, up, right, and down, take the agent to states 12, 13, 14, and 15, respectively. Assume that the transitions from the original states are unchanged. What, then, is $v_\pi(15)$ for the equiprobable random policy? Now suppose the dynamics of state 13 are also changed, such that action down from state 13 takes the agent to the new state 15. What is $v_\pi(15)$ for the equiprobable random policy in this case?

**My answer:**

For the case that the transitions from the original states are unchanged:

$$
\begin{aligned}
v_\pi(15) &= \sum_a \pi(a | 15) \sum_{s^\prime, r} p(s^\prime, r | 15, a) \big[r + v_\pi(s^\prime) \big] \\
&= 0.25 \big[-1 + v_\pi(12) \big] + 0.25 \big[-1 + v_\pi(13) \big] + 0.25 \big[-1 + v_\pi(14) \big] + 0.25 \big[-1 + v_\pi(15) \big] \\
&= -1 + 0.25 \big[-22 - 20 - 14 + v_\pi(15) \big] \\
&= -15 + 0.25 v_\pi(15) \\
&= \frac{-15}{0.75} \\
&= -20
\end{aligned}
$$

For the case that the transitions from the original states are changed:

TODO: Write program for iterative policy evaluation - start with replicating the $v_\pi$ table in the book
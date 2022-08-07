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

For the case where the transitions from state 13 are changed:

I wrote a program implementing iterative policy evaluation for this example. It got the same results as in the book for the original example and validated $v_\pi(15) = -20$ for the case that transitions from the original states are unchanged. When running the program for the case where transitions for state 13 are changed I found that the state values didn't change. This makes sense, since the state values for the next state after selecting an action is identical for state 13 and state 15. Thus we still have:

$$
v_\pi(15) = -20
$$

## Exercise 4.3

What are the equations analogous to (4.3), (4.4), and (4.5), but for action-value functions instead of state-value functions?

**My answer:**

$$
\begin{aligned}
q_\pi(s, a) &= \mathbb{E}_\pi[G_t | S_t = s, A_t = a] \\
&= \mathbb{E}_\pi[R_t + \gamma G_{t+1} | S_t = s, A_t = a] \\
&= \mathbb{E}[R_t + \gamma v_\pi(S_{t+1}) | S_t = s, A_t = a] \\
&= \mathbb{E}[R_t + \gamma \sum_{a^\prime \in \mathcal{A}(S_{t+1})} \pi(a^\prime | S_{t+1})q_\pi(S_{t+1}, a^\prime) | S_t = s, A_t = a] \\
&= \sum_{s^\prime, r} p(s^\prime, r | s, a) \big[r + \gamma \sum_{a^\prime} \pi(a^\prime | s^\prime) q_\pi(s^\prime, a^\prime) \big]
\end{aligned}
$$

$$
\begin{aligned}
q_{k+1}(s, a) &= \mathbb{E}[R_t + \gamma \sum_{a^\prime \in \mathcal{A}(S_{t+1})} \pi(a^\prime | S_{t+1})q_k(S_{t+1}, a^\prime) | S_t = s, A_t = a] \\
&= \sum_{s^\prime, r} p(s^\prime, r | s, a) \big[r + \gamma \sum_{a^\prime} \pi(a^\prime | s^\prime) q_k(s^\prime, a^\prime) \big]
\end{aligned}
$$

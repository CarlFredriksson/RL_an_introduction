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

## Exercise 4.4

The policy iteration algorithm on page 80 has a subtle bug in that it may never terminate if the policy continually switches between two or more policies that are equally good. This is okay for pedagogy, but not for actual use. Modify the pseudocode so that convergence is guaranteed.

**My answer:**

1. Initialization
    * $V(s) \in \mathbb{R}$ and $\pi(s) \in \mathcal{A}(s)$ arbitrarily for all $s \in \mathcal{S}; V(terminal) = 0$
2. Policy Evaluation
    * Loop:
        * $\Delta \leftarrow 0$
        * Loop for each $s \in \mathcal{S}$:
            * $v \leftarrow V(s)$
            * $V(s) \leftarrow \sum_{s^\prime, r} p(s^\prime, r | s, \pi(s)) \big[r + \gamma V(s^\prime) \big]$
            * $\Delta \leftarrow \max(\Delta, |v - V(s)|)$
    * until $\Delta < \theta$ (a small positive number determining the accuracy of estimation)
3. Policy Improvement
    * $\textit{policy-stable} \leftarrow true$
    * For each $s \in \mathcal{S}$:
        *  $\textit{old-action} \leftarrow \pi(s)$
        *  $\pi(s) \leftarrow \argmax_a \sum_{s^\prime, r} p(s^\prime, r | s, a)\big[r + \gamma V(s^\prime) \big]$
        *  $Q(s, \pi(s)) \leftarrow \sum_{s^\prime, r} p(s^\prime, r | s, \pi(s))\big[r + \gamma V(s^\prime) \big]$
        *  If $Q(s, \pi(s)) > V(s)$, then $\textit{policy-stable} \leftarrow false$
    * If $\textit{policy-stable}$, then stop and return $V \approx v_*$ and $\pi \approx \pi_*$; else go to 2

## Exercise 4.5

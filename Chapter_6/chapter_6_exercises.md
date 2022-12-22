# Exercises - Chapter 6

Carl Fredriksson, c@msp.se

## Exercise 6.1

If $V$ changes during the episode, then (6.6) only holds approximately; what would the difference be between the two sides? Let $V_t$ denote the array of state values used at time $t$ in the TD error (6.5) and in the TD update (6.2). Redo the derivation above to determine the additional amount that must be added to the sum of TD errors in order to equal the Monte Carlo error.

**My answer:**

$$
\begin{aligned}
G_t - V_t(S_t) &= R_{t+1} + \gamma G_{t+1} - V_t(S_t) + \gamma V_t(S_{t+1}) - \gamma V_t(S_{t+1}) \\
&= \delta_t + \gamma \big[G_{t+1} - V_t(S_{t+1}) \big] \\
&= \delta_t + \gamma \big[G_{t+1} - V_t(S_{t+1}) + V_{t+1}(S_{t+1}) - V_{t+1}(S_{t+1}) \big] \\
&= \delta_t + \gamma \big[G_{t+1} - V_{t+1}(S_{t+1}) \big] + \gamma \big[V_{t+1}(S_{t+1}) - V_t(S_{t+1}) \big] \\
&= \delta_t + \gamma \delta_{t+1} + \gamma \big[V_{t+1}(S_{t+1}) - V_t(S_{t+1}) \big] + \gamma^2 \big[G_{t+2} - V_t(S_{t+2}) \big] \\
&= \delta_t + \gamma \delta_{t+1} + \gamma \big[V_{t+1}(S_{t+1}) - V_t(S_{t+1}) \big] + \gamma^2 \delta_{t+2} + \gamma^2 \big[V_{t+2}(S_{t+2}) - V_t(S_{t+2}) \big] + \\ &\quad \dots + \gamma^{T-t-1} \delta_{T-1} + \gamma^{T-t-1} \big[V_{T-1}(S_{T-1}) - V_t(S_{T-1}) \big] + \gamma^{T-t} \big[G_T - V_t(S_{T}) \big] \\
&= \delta_t + \gamma \delta_{t+1} + \gamma \big[V_{t+1}(S_{t+1}) - V_t(S_{t+1}) \big] + \gamma^2 \delta_{t+2} + \gamma^2 \big[V_{t+2}(S_{t+2}) - V_t(S_{t+2}) \big] + \\ &\quad \dots + \gamma^{T-t-1} \delta_{T-1} + \gamma^{T-t-1} \big[V_{T-1}(S_{T-1}) - V_t(S_{T-1}) \big] + \gamma^{T-t} \big[0 - 0 \big] \\
&= \sum_{k=t}^{T-1} \gamma^{k-t} \delta_k + \sum_{k=t+1}^{T-1} \gamma^{k-t} \big[V_k(S_k) - V_t(S_k) \big] 
\end{aligned}
$$

Thus the additional amount that must be added is:

$$
\sum_{k=t+1}^{T-1} \gamma^{k-t} \big[V_k(S_k) - V_t(S_k) \big] 
$$

## Exercise 6.2

This is an exercise to help develop your intuition about why TD methods are often more efficient than Monte Carlo methods. Consider the driving home example and how it is addressed by TD and Monte Carlo methods. Can you imagine a scenario in which a TD update would be better on average than a Monte Carlo update? Give an example scenario—a description of past experience and a current state—in which you would expect the TD update to be better. Here's a hint: Suppose you have lots of experience driving home from work. Then you move to a new building and a new parking lot (but you still enter the highway at the same place). Now you are starting to learn predictions for the new building. Can you see why TD updates are likely to be much better, at least initially, in this case? Might the same sort of thing happen in the original scenario?

**My answer:**

I can't think of an easy answer for the hint-scenario. I feel like I'm lacking information - it seems that it would be affected by the reward variance, $\alpha$, and how we initialize the new states for example?

One scenario I can think of where a TD update would be better: If we observe an extreme reward in an episode, that outlier will affect the value estimate for only one state in one TD update, but it will affect the estimate for all states visited before that reward was received in one Monte Carlo update.

## Exercise 6.3

From the results shown in the left graph of the random walk example it appears that the first episode results in a change in only $V(A)$. What does this tell you about what happened on the first episode? Why was only the estimate for this one state changed? By exactly how much was it changed?

**My answer:**

The first episode terminated on the left side. Only $V(A)$ was changed since the TD error was 0 for all other states:

$$
\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t) = 0 + 0.5 - 0.5 = 0
$$

$$
V(S_t) \leftarrow V(S_t) + \alpha [R_{t+1} + \gamma V(S_{t+1}) - V(S_t)] = 0.5 + 0.1 \cdot 0 = 0.5
$$

The TD error for $t = T-1$ where $S_t = A$:

$$
\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t) = R_T + \gamma V(S_T) - V(A) = 0 + 0 - 0.5 = -0.5
$$

Thus we have only one relevant update:

$$
V(A) \leftarrow V(A) + \alpha [R_T + \gamma V(S_T) - V(A)] = 0.5 + 0.1 (-0.5) = 0.45
$$

The estimate for $V(A)$ was changed by -0.05.

## Exercise 6.4

The specific results shown in the right graph of the random walk example are dependent on the value of the step-size parameter, $\alpha$. Do you think the conclusions about which algorithm is better would be affected if a wider range of $\alpha$ values were used? Is there a different, fixed value of $\alpha$ at which either algorithm would have performed significantly better than shown? Why or why not?

**My answer:**

With $\alpha = 0$, both algorithms would be stuck with the initial estimates (but 0 is probably not in the set of possible values for $\alpha$).

I don't think there is a fixed value of $\alpha$ at which either algorithm would have performed significantly better than shown. With larger $\alpha$, the algorithms initially learn quicker, but will stop improving quicker compared to smaller $\alpha$, due to larger indefinite fluctuations. In order to significantly improve, I believe that we need a dynamic $\alpha$ that starts of large in order to quickly learn better estimates than the initial estimates, but gets smaller over time and eventually reaches 0 in order to remove the indefinite fluctuations.

## Exercise 6.5

In the right graph of the random walk example, the RMS error of the TD method seems to go down and then up again, particularly at high $\alpha$’s. What could have caused this? Do you think this always occurs, or might it be a function of how the approximate value function was initialized?

**My answer:**

The value estimates other than $V(C)$ will quickly improve in the beginning due their initializations differing significantly from their true values. However, the estimates will never converge to their true values due to the recency bias caused by the fixed value $\alpha$.

It will take some episodes before $V(C)$ starts to get updated, and when it does it will become a worse estimate. Due to initializing all estimates to 0.5, which is the true value for $V(C) = v_\pi(C) = 0.5$, it can't become a better estimate. It will move towards $V(B)$ in some updates and towards $V(D)$ in others.

Thus I believe it might be a function of how the approximate value function (the value estimates) was initialized.

## Exercise 6.6

In Example 6.2 we stated that the true values for the random walk example are $\frac{1}{6}$, $\frac{2}{6}$, $\frac{3}{6}$, $\frac{4}{6}$, $\frac{5}{6}$, $\frac{1}{6}$, for states $A$ through $E$. Describe at least two different ways that these could have been computed. Which would you guess we actually used? Why?

**My answer:**

On option is to use Monte Carlo prediction with sample averaging (first-visit or every-visit), which will converge to the true values $v_\pi$ (unlike using a fixed value $\alpha$). However, convergence is only guaranteed in the limit.

A better option is to use value/policy iteration from dynamic programming. However, this requires specifying the dynamics function of the problem.

Since the state space is so small and the dynamics so simple, I believe the best method (and probably the one the authors used) is to simply solve the Bellman equation:

$$
v_\pi(s) = \sum_{a \in \mathcal{A}(s)} \pi(a | s) \sum_{s^\prime, r} p(s^\prime, r | s, a) \big[r + \gamma v_\pi(s^\prime) \big], \quad \text{for all} \; s \in \mathcal{S}
$$

Since it's a Markov reward process (an MDP without actions), we can simplify:

$$
v_\pi(s) = \sum_{s^\prime, r} p(s^\prime, r | s) \big[r + \gamma v_\pi(s^\prime) \big], \quad \text{for all} \; s \in \mathcal{S}
$$

Inputting the dynamics of the problem, we end up with the following system of linear equations:

$$
\begin{aligned}
v_\pi(A) &= \frac{1}{2} v_\pi(B) \\
v_\pi(B) &= \frac{1}{2} v_\pi(A) + \frac{1}{2} v_\pi(C) \\
v_\pi(C) &= \frac{1}{2} v_\pi(B) + \frac{1}{2} v_\pi(D) \\
v_\pi(D) &= \frac{1}{2} v_\pi(C) + \frac{1}{2} v_\pi(E) \\
v_\pi(E) &= \frac{1}{2} v_\pi(D) + \frac{1}{2} \\
\end{aligned}
$$

which can easily be solved by hand.

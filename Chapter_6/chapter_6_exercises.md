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

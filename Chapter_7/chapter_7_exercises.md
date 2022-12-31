# Exercises - Chapter 7

Carl Fredriksson, c@msp.se

## Exercise 7.1

In Chapter 6 we noted that the Monte Carlo error can be written as the sum of TD errors (6.6) if the value estimates don't change from step to step. Show that the n-step error used in (7.2) can also be written as a sum of TD errors (again if the value estimates don't change) generalizing the earlier result.

**My answer:**

$$
\begin{aligned}
G_{t:t+n} - V(S_t) &= R_{t+1} + \gamma G_{t+1:t+n} - V(S_t) + \gamma V(S_{t+1}) - \gamma V(S_{t+1}) \\
&= \delta_t + \gamma \big[G_{t+1:t+n} - V(S_{t+1}) \big] \\
&= \delta_t + \gamma \delta_{t+1} + \gamma^2 \big[G_{t+2:t+n} - V(S_{t+2}) \big]  \\ 
&= \delta_t + \gamma \delta_{t+1} + \gamma^2 \delta_{t+2} + \dots + \gamma^{n-1} \big[G_{t+n-1:t+n} - V(S_{t+n-1}) \big] \\
&= \delta_t + \gamma \delta_{t+1} + \gamma^2 \delta_{t+2} + \dots + \gamma^{n-1} \big[R_{t+n} + \gamma V(S_{t+n}) - V(S_{t+n-1}) \big] \\
&= \delta_t + \gamma \delta_{t+1} + \gamma^2 \delta_{t+2} + \dots + \gamma^{n-1} \delta_{t+n-1} \\
&= \sum_{k=t}^{t+n-1} \gamma^{k-t} \delta_k
\end{aligned}
$$

## Exercise 7.2

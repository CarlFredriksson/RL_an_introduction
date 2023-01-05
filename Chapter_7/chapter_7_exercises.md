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

## Exercise 7.2 (programming)

With an n-step method, the value estimates do change from step to step, so an algorithm that used the sum of TD errors (see previous exercise) in place of the error in (7.2) would actually be a slightly different algorithm. Would it be a better algorithm or a worse one? Devise and program a small experiment to answer this question empirically.

**My answer:**

I programmed an experiment using the 4x4 gridworld in Example 4.1. There was a big difference in convergence speed when comparing the n-step methods to TD(0). However, I did not see any significant difference between n-step TD and n-step sum of TD errors. A constant step size of $\alpha = 0.001$ was used for all algorithms and the results were averaged over 10 runs per algorithm.

![Ex 7.2 Gridworld Result](Exercise_7_2/gridworld_result.png)

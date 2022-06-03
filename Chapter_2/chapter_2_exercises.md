# Exercises - Chapter 2

Carl Fredriksson, c@msp.se

## Exercise 2.1 

In $\epsilon$-greedy action selection, for the case of two actions and $\epsilon = 0.5$, what is the probability that the greedy action is selected?

**My answer:**

Let $n_a$ be the number of actions. Any any time step we can either explore or exploit. The probability of selecting the greedy action is:

$$
\begin{equation}
\begin{split}
P(\textit{select greedy action}) &= P(exploit) * P(\textit{select greedy action} | exploit) + P(explore) * P(\textit{select greedy action} | explore) \\
&= (1 - \epsilon) \cdot 1 + \epsilon \cdot \frac{1}{n_a} \\
&= 0.5 + 0.5 \cdot 0.5 \\
&= 0.75
\end{split}
\end{equation}
$$

## 

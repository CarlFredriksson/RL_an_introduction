# Exercises - Chapter 2

Carl Fredriksson, c@msp.se

## Exercise 2.1 

In $\epsilon$-greedy action selection, for the case of two actions and $\epsilon = 0.5$, what is the probability that the greedy action is selected?

**My answer:**

Let $n_a$ be the number of actions. Any any time step we can either explore or exploit. The probability of selecting the greedy action is:

$$
\begin{equation}
\begin{split}
P(\textit{select greedy action}) &= P(exploit)P(\textit{select greedy action} | exploit) + P(explore)P(\textit{select greedy action} | explore) \\
&= (1 - \epsilon) \cdot 1 + \epsilon \cdot \frac{1}{n_a} \\
&= 0.5 + 0.5 \cdot 0.5 \\
&= 0.75
\end{split}
\end{equation}
$$

## Exercise 2.2: Bandit example

Consider a $k$-armed bandit problem with $k = 4$ actions, denoted 1, 2, 3, and 4. Consider applying to this problem a bandit algorithm using $\epsilon$-greedy action selection, sample-average action-value estimates, and initial estimates of $Q_1(a) = 0$, for all $a$. Suppose the initial sequence of actions and rewards is $A_1 = 1$, $R_1 = 1$, $A_2 = 2$, $R_2 = 1$, $A_3 = 2$, $R_3 = 2$, $A_4 = 2$, $R_4 = 2$, $A_5 = 3$, $R_5 = 0$. On some of these time steps the $\epsilon$ case may have occurred, causing an action to be selected at random. On which time steps did this definitely occur? On which time steps could this possibly have occurred?

**My answer:**

|$t$|$A_t$|$R_t$|$Q_t(1)$|$Q_t(2)$|$Q_t(3)$|$Q_t(4)$|$\epsilon$ case|
|:-:|:---:|:---:|:------:|:------:|:------:|:------:|:-------------:|
| 0 |  -  |  -  |   0    |   0    |   0    |   0    |       -       |
| 1 |  1  |  1  |   1    |   0    |   0    |   0    |    possibly   |
| 2 |  2  |  1  |   1    |   1    |   0    |   0    |      yes      |
| 3 |  2  |  2  |   1    |   3/2  |   0    |   0    |    possibly   |
| 4 |  2  |  2  |   1    |   5/3  |   0    |   0    |    possibly   |
| 5 |  3  |  0  |   1    |   5/3  |   0    |   0    |      yes      |

## Exercise 2.3

In the comparison shown in Figure 2.2, which method will perform best in the long run in terms of cumulative reward and probability of selecting the best action? How much better will it be? Express your answer quantitatively.

**My answer:**

In the long run, both $\epsilon$-greedy methods will have found the optimal action and the only difference between the two will be the frequency of exploration. The method with $\epsilon = 0.01$ will outperform the method with $\epsilon = 0.1$ due to selecting the optimal action 99% of the time compared to 90% of the time. It will be 10% better since $0.99/0.9 = 1.1$.

## Exercise 2.4

If the step-size parameters, $\alpha{_n}$, are not constant, then the estimate $Q_n$ is a weighted average of previously received rewards with a weighting different from that given by (2.6). What is the weighting on each prior reward for the general case, analogous to (2.6), in terms of the sequence of step-size parameters?

**My answer:**

$$
\begin{equation}
\begin{split}
Q_{n+1} &= Q_n + \alpha_n (R_n - Q_n) \\
&= \alpha_n R_n + (1 - \alpha_n) Q_n \\
&= \alpha_n R_n + (1 - \alpha_n) (\alpha_{n-1} R_{n-1} + [1 - \alpha_{n-1}] Q_{n-1}) \\
&= \alpha_n R_n + (1 - \alpha_n) \alpha_{n-1} R_{n-1} + (1 - \alpha_n) (1 - \alpha_{n-1}) Q_{n-1} \\
&= \alpha_n R_n + (1 - \alpha_n) \alpha_{n-1} R_{n-1} + (1 - \alpha_n) (1 - \alpha_{n-1}) \alpha_{n-2} R_{n-2} + \\
&\qquad \dots + \prod_{i=2}^{n} (1 - \alpha_i) \alpha_1 R_1 + \prod_{i=1}^{n} (1 - \alpha_i) Q_1 \\
&= \prod_{i=1}^{n} (1 - \alpha_i) Q_1 + \alpha_n R_n + \sum_{i=1}^{n-1} \bigg[\prod_{j=i+1}^{n} (1 - \alpha_j) \bigg] \alpha_i R_i
\end{split}
\end{equation}
$$

## Exercise 2.5 (programming)

TODO: Insert plots from the program and maybe some notes?
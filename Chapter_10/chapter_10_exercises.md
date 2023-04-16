# Exercises - Chapter 10

Carl Fredriksson, c@msp.se

## Exercise 10.1

We have not explicitly considered or given pseudocode for any Monte Carlo methods in this chapter. What would they be like? Why is it reasonable not to give pseudocode for them? How would they perform on the Mountain Car task?

**My answer:**

> What would they be like?

Generate episodes in the same way, but update value estimates only in between episodes using full returns from the previous episode.

> Why is it reasonable not to give pseudocode for them?

Because they are special cases of $n$-step Sarsa (by setting $n$ to be the length of the the episodes).

> How would they perform on the Mountain Car task?

Poorly. The performance seems to be best for intermediate levels of bootstrapping (peaking at $n=4$). Larger $n$ leads to worse performance, and as mentioned above, Monte Carlo (MC) methods are equivalent to the extreme case with the maximum $n$. We can also reason about how the episodes would play out. With MC methods and $\textbf{w}$ initialized to $\textbf{0}$, we would have very long early episodes. Since updates are only made after reaching the terminal state, action selection would be completely random for the entirety of the first episode, which would be incredibly long for the majority of runs.

## Exercise 10.2

Give pseudocode for semi-gradient one-step *Expected* Sarsa for control.

**My answer:**

* Input: a differentiable action-value function parameterization $\hat{q}:\mathcal{S} \times \mathcal{A} \times \mathbb{R}^d \rightarrow \mathbb{R}$
* Input: a policy $\pi$ (if estimating $q_\pi$)
* Algorithm parameters: step size $\alpha > 0$, small $\epsilon > 0$
* Initialize value-function weights $\textbf{w} \in \mathbb{R}^d$ arbitrarily (e.g., $\textbf{w} = \textbf{0}$)
* Loop for each episode:
  * Initialize $S \not ={terminal}$
  * Loop for each step of episode$
    * Select $A \sim \pi(\cdot|S)$ or $\epsilon$-greedy wrt $\hat{q}(S,\cdot,\textbf{w})$
    * Take action $A$, observe $R, S^\prime$
    * $\textbf{w} \leftarrow \textbf{w} + \alpha \big[R + \sum_a \pi(a|S^\prime) \hat{q}(S^\prime,a,\textbf{w}) - \hat{q}(S,A,\textbf{w})\big] \nabla \hat{q}(S,A,\textbf{w})$
    * $S \leftarrow S^\prime$
    * If $S$ is terminal:
      * Go to next episode

## Exercise 10.3

Why do the results shown in Figure 10.4 have higher standard errors at large $n$ than at small $n$?

**My answer:**

I think it's due to larger $n$ resulting in more possible trajectories per update, thus increasing the variance.

## Exercise 10.4

Give pseudocode for a differential version of semi-gradient Q-learning.

**My answer:**

* Input: a differentiable action-value function parametrization $\hat{q}:\mathcal{S} \times \mathcal{A} \times \mathbb{R}^d \rightarrow \mathbb{R}$
* Algorithm parameters: step sizes $\alpha,\beta > 0$, small $\epsilon > 0$
* Initialize value-function weights $\textbf{w} \in \mathbb{R}^d$ arbitrarily (e.g., $\textbf{w} = \textbf{0}$)
* Initialize average reward estimate $\overline{R} \in \mathbb{R}$ arbitrarily (e.g., $\overline{R} = 0$)
* Initialize state $S$
* Loop for each step:
  * Choose $A$ as a function of $\hat{q}(S,\cdot,\textbf{w})$ (e.g., $\epsilon$-greedy)
  * Take action $A$, observe $R,S^\prime$
  * $\delta \leftarrow R - \overline{R} + \max_a \hat{q}(S^\prime, a, \textbf{w}) - \hat{q}(S, A, \textbf{w})$
  * $\overline{R} \leftarrow \overline{R} + \beta \delta$
  * $\textbf{w} \leftarrow \textbf{w} + \alpha \delta \nabla \hat{q}(S,A,\textbf{w})$
  * $S \leftarrow S^\prime$

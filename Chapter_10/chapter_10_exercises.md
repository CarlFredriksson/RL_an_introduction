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

## Exercise 10.5

What equations are needed (beyond 10.10) to specify the differential version of TD(0)?

**My answer:**

$\overline{R}$-update:

$$
\overline{R}_{t+1} \leftarrow \overline{R}_t + \beta \delta_t
$$

$\textbf{w}$-update:

$$
\textbf{w}_{t+1} \leftarrow \textbf{w}_t + \alpha \delta_t \nabla \hat{v}(S_t,\textbf{w}_t)
$$

## Exercise 10.6

Suppose there is an MDP that under any policy produces the deterministic sequence of rewards $+1,0,+1,0,+1,0,\dots$ going on forever. Technically, this violates ergodicity; there is no stationary limiting distribution $\mu_\pi$ and the limit (10.7) does not exist. Nevertheless, the average reward (10.6) is well defined. What is it? Now consider two states in this MDP. From $A$, the reward sequence is exactly as described above, starting with a $+1$, whereas, from $B$, the reward sequence starts with a $0$ and then continues with $+1,0,+1,0,\dots$ We would like to compute the differential values of $A$ and $B$. Unfortunately, the differential return (10.9) is not well defined when starting from these states as the implicit limit does not exist. To repair this, one could alternatively define the differential value of a state as

$$
\begin{aligned}
v_\pi(s) \overset{.}{=} \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h \gamma^t \bigg(\mathbb{E}_\pi[R_{t+1}|S_0=s] - r(\pi)\bigg)
\end{aligned}
$$

Under this definition, what are the differential values of states $A$ and $B$?

**My answer:**

> Nevertheless, the average reward (10.6) is well defined. What is it?

$$
\begin{aligned}
r(\pi) &\overset{.}{=} \lim_{h \to \infty} \frac{1}{h} \sum_{t=1}^h \mathbb{E}[R_{t+1}|S_0,A_{0:t-1} \sim \pi] \\
&= \lim_{h \to \infty} \frac{1}{h} \sum_{t=1}^{h/2} 1+0 \\
&= \frac{1}{2}
\end{aligned}
$$

> Under this definition, what are the differential values of states $A$ and $B$?

$$
\begin{aligned}
v_\pi(A) &= \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h \gamma^t \bigg(\mathbb{E}_\pi[R_{t+1}|S_0=A] - r(\pi)\bigg) \\
&= \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h \gamma^t \bigg(\mathbb{E}_\pi[R_{t+1}|S_0=A] - \frac{1}{2}\bigg) \\
&= \lim_{\gamma \to 1} \bigg[\gamma^0(1 - \frac{1}{2}) + \gamma^1(0 - \frac{1}{2}) + \gamma^2(1 - \frac{1}{2}) + \gamma^3(0 - \frac{1}{2}) + \dots\bigg] \\
&= \frac{1}{2} \lim_{\gamma \to 1} \bigg[1 - \gamma + \gamma^2 - \gamma^3 + \dots\bigg] \\
&= \frac{1}{2} \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h (-1)^t \gamma^t \\
&= \frac{1}{2} \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h (-\gamma)^t \\
&= \frac{1}{2} \lim_{\gamma \to 1} \frac{1}{1-(-\gamma)} \\
&= \frac{1}{2} \lim_{\gamma \to 1} \frac{1}{1+\gamma} \\
&= \frac{1}{4} \\
\end{aligned}
$$

$$
\begin{aligned}
v_\pi(B) &= \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h \gamma^t \bigg(\mathbb{E}_\pi[R_{t+1}|S_0=B] - r(\pi)\bigg) \\
&= \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h \gamma^t \bigg(\mathbb{E}_\pi[R_{t+1}|S_0=B] - \frac{1}{2}\bigg) \\
&= \lim_{\gamma \to 1} \bigg[\gamma^0(0 - \frac{1}{2}) + \gamma^1(1 - \frac{1}{2}) + \gamma^2(0 - \frac{1}{2}) + \gamma^3(1 - \frac{1}{2}) + \dots\bigg] \\
&= \frac{1}{2} \lim_{\gamma \to 1} \bigg[-1 + \gamma - \gamma^2 + \gamma^3 - \dots\bigg] \\
&= \frac{1}{2} \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h (-1)^{t+1} \gamma^t \\
&= -\frac{1}{2} \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h (-1)^t \gamma^t \\

&= -\frac{1}{4} \\
\end{aligned}
$$

## Exercise 10.7

Consider a Markov reward process consisting of a ring of three states $A$, $B$, and $C$, with state transitions going deterministically around the ring. $A$ reward of $+1$ is received upon arrival in $A$ and otherwise the reward is $0$. What are the differential values of the three states, using (10.13)?

**My answer:**

$$
r(\pi) = \frac{1}{3}
$$

$$
\begin{aligned}
v_\pi(A) &= \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h \gamma^t \bigg(\mathbb{E}_\pi[R_{t+1}|S_0=A] - r(\pi)\bigg) \\
&= \lim_{\gamma \to 1} \lim_{h \to \infty} \sum_{t=0}^h \gamma^t \bigg(\mathbb{E}_\pi[R_{t+1}|S_0=A] - \frac{1}{3}\bigg) \\
&= \lim_{\gamma \to 1} \bigg[\gamma^0(0 - \frac{1}{3}) + \gamma^1(0 - \frac{1}{3}) + \gamma^2(1 - \frac{1}{3}) + \gamma^3(0 - \frac{1}{3}) + \gamma^4(0 - \frac{1}{3}) + \gamma^5(1 - \frac{1}{3}) + \dots\bigg] \\
&= \frac{1}{3} \lim_{\gamma \to 1} \bigg[-1 - \gamma + 2\gamma^2 - \gamma^3 - \gamma^4 + 2\gamma^5 - \dots\bigg] \\
&= \frac{1}{3} \lim_{\gamma \to 1} \bigg[(-1-\gamma-\gamma^3-\dots) + 2(\gamma^2+\gamma^5+\gamma^8+\dots)\bigg] \\
&= \lim_{\gamma \to 1} \bigg[\frac{1}{3}(-1-\gamma-\gamma^2-\dots) + \gamma^2(1+\gamma^3+\gamma^6+\dots)\bigg] \\
&= \lim_{\gamma \to 1} \bigg[-\frac{1}{3} \lim_{h\to\infty} \sum_{t=0}^h \gamma^t + \gamma^2 \lim_{h\to\infty} \sum_{t=0}^h (\gamma^3)^t\bigg] \\
&= \lim_{\gamma \to 1} \bigg[-\frac{1}{3(1-\gamma)} + \frac{\gamma^2}{(1-\gamma^3)}\bigg] \\
&= \lim_{\gamma \to 1} \frac{3\gamma^2(1-\gamma) - (1-\gamma^3)}{3(1-\gamma)(1-\gamma^3)} \\
&= \frac{1}{3} \lim_{\gamma \to 1} \frac{(\gamma-1)^2(-2\gamma-1)}{(\gamma-1)^2(\gamma^2+\gamma+1)} \\
&= \frac{1}{3} \lim_{\gamma \to 1} \frac{-2\gamma-1}{\gamma^2+\gamma+1} \\
&= -\frac{1}{3}
\end{aligned}
$$

$$
\begin{aligned}
v_\pi(B) &= \lim_{\gamma \to 1} \bigg[\gamma^0(0 - \frac{1}{3}) + \gamma^1(1 - \frac{1}{3}) + \gamma^2(0 - \frac{1}{3}) + \dots\bigg] \\
&= \frac{1}{3} \lim_{\gamma \to 1} \bigg[-1 + 2\gamma - \gamma^2 - \dots\bigg] \\
&= \frac{1}{3} \lim_{\gamma \to 1} \bigg[(-1-\gamma^2-\gamma^3-\dots) + 2(\gamma+\gamma^4+\gamma^7+\dots)\bigg] \\
&= \lim_{\gamma \to 1} \bigg[\frac{1}{3}(-1-\gamma-\gamma^2-\dots) + \gamma(1+\gamma^3+\gamma^6+\dots)\bigg] \\
&= \lim_{\gamma \to 1} \bigg[-\frac{1}{3(1-\gamma)} + \frac{\gamma}{(1-\gamma^3)}\bigg] \\
&= \lim_{\gamma \to 1} \frac{3\gamma(1-\gamma) - (1-\gamma^3)}{3(1-\gamma)(1-\gamma^3)} \\
&= \frac{1}{3} \lim_{\gamma \to 1} \frac{(\gamma-1)^3}{(\gamma-1)^2(\gamma^2+\gamma+1)} \\
&= \frac{1}{3} \lim_{\gamma \to 1} \frac{\gamma-1}{\gamma^2+\gamma+1} \\
&= 0
\end{aligned}
$$

$$
\begin{aligned}
v_\pi(C) &= \lim_{\gamma \to 1} \bigg[\gamma^0(1 - \frac{1}{3}) + \gamma^1(0 - \frac{1}{3}) + \gamma^2(0 - \frac{1}{3}) + \dots\bigg] \\
&= \frac{1}{3} \lim_{\gamma \to 1} \bigg[2 - \gamma - \gamma^2 - \dots\bigg] \\
&= \lim_{\gamma \to 1} \bigg[\frac{1}{3}(-1-\gamma-\gamma^2-\dots) + (1+\gamma^3+\gamma^6+\dots)\bigg] \\
&= \lim_{\gamma \to 1} \bigg[-\frac{1}{3(1-\gamma)} + \frac{1}{(1-\gamma^3)}\bigg] \\
&= \lim_{\gamma \to 1} \frac{3(1-\gamma) - (1-\gamma^3)}{3(1-\gamma)(1-\gamma^3)} \\
&= \frac{1}{3} \lim_{\gamma \to 1} \frac{(\gamma-1)^2(\gamma+2)}{(\gamma-1)^2(\gamma^2+\gamma+1)} \\
&= \frac{1}{3} \lim_{\gamma \to 1} \frac{\gamma+2}{\gamma^2+\gamma+1} \\
&= \frac{1}{3}
\end{aligned}
$$

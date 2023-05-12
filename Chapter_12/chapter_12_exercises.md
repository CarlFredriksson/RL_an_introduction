# Exercises - Chapter 12

Carl Fredriksson, c@msp.se

## Exercise 12.1

Just as the return can be written recursively in terms of the first reward and itself one-step later (3.9), so can the $\lambda$-return. Derive the analogous recursive relationship from (12.2) and (12.1).

**My answer:**

$$
\begin{aligned}
G_t^\lambda &\overset{.}{=} (1-\lambda) \sum_{n=1}^\infty \lambda^{n-1} G_{t:t+n} \\
&= (1-\lambda) \bigg(G_{t:t+1} + \lambda G_{t:t+2} + \lambda^2 G_{t:t+3} + \dots\bigg) \\
&= (1-\lambda) \bigg(\big[R_{t+1} + \gamma \hat{v}(S_{t+1}, \textbf{w}_t)\big] + \lambda \big[R_{t+1} + \gamma R_{t+2} + \gamma^2 \hat{v}(S_{t+2}, \textbf{w}_{t+1})\big] + \lambda^2 \big[R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \gamma^3 \hat{v}(S_{t+3}, \textbf{w}_{t+2})\big] + \dots\bigg) \\
&= (1-\lambda) R_{t+1} \bigg(\sum_{n=0}^\infty \gamma^n\bigg) + (1-\lambda) \gamma \hat{v}(S_{t+1}, \textbf{w}_t) + (1-\lambda) \bigg(\lambda\big[\gamma R_{t+2} + \gamma^2 \hat{v}(S_{t+2}, \textbf{w}_{t+1})\big] + \lambda^2 \big[\gamma R_{t+2} + \gamma^2 R_{t+3} + \gamma^3 \hat{v}(S_{t+3}, \textbf{w}_{t+2})\big] + \dots\bigg) \\
&= \frac{(1-\lambda)}{(1-\lambda)} R_{t+1} + (1-\lambda) \gamma \hat{v}(S_{t+1}, \textbf{w}_t) + (1-\lambda)\lambda\gamma \bigg(\big[R_{t+2} + \gamma \hat{v}(S_{t+2}, \textbf{w}_{t+1})\big] + \lambda \big[R_{t+2} + \gamma R_{t+3} + \gamma^2 \hat{v}(S_{t+3}, \textbf{w}_{t+2})\big] + \dots\bigg) \\
&= R_{t+1} + (1-\lambda) \gamma \hat{v}(S_{t+1}, \textbf{w}_t) + \lambda\gamma(1-\lambda) \sum_{n=1}^\infty \lambda^{n-1} G_{t+1:t+1+n} \\
&= R_{t+1} + (1-\lambda) \gamma \hat{v}(S_{t+1}, \textbf{w}_t) + \lambda\gamma G_{t+1}^\lambda
\end{aligned}
$$

## Exercise 12.2

The parameter $\lambda$ characterizes how fast the exponential weighting in Figure 12.2 falls off, and thus how far into the future the $\lambda$-return algorithm looks in determining its update. But a rate factor such as  is sometimes an awkward way of characterizing the speed of the decay. For some purposes it is better to specify a time constant, or half-life. What is the equation relating $\lambda$ and the half-life, $\tau_\lambda$, the time by which the weighting sequence will have fallen to half of its initial value?

**My answer:**

$$
\begin{aligned}
(1-\lambda)\lambda^\tau &= (1-\lambda)\frac{1}{2} \\
\lambda^\tau &= \frac{1}{2} \\
\tau &= \log_\lambda(\frac{1}{2})
\end{aligned}
$$

$$
\begin{aligned}
\tau_\lambda = t + \tau + 1 = t + \log_\lambda(\frac{1}{2}) + 1
\end{aligned}
$$

Adding 1 since the $n$-step return $G_{t:t+n}$ is weighted by $\lambda^{n-1}$.

## Exercise 12.3

Some insight into how TD($\lambda$) can closely approximate the off-line $\lambda$-return algorithm can be gained by seeing that the latter’s error term (in brackets in (12.4)) can be written as the sum of TD errors (12.6) for a single fixed $\textbf{w}$. Show this, following the pattern of (6.6), and using the recursive relationship for the $\lambda$-return you obtained in Exercise 12.1.

**My answer:**

$$
\begin{aligned}
G_t^\lambda - \hat{v}(S_t,\textbf{w}) &= R_{t+1} + (1-\lambda) \gamma \hat{v}(S_{t+1}, \textbf{w}) + \lambda\gamma G_{t+1}^\lambda - \hat{v}(S_t,\textbf{w}) \\
&= R_{t+1} + \gamma \hat{v}(S_{t+1}, \textbf{w}) - \hat{v}(S_t,\textbf{w}) + \lambda\gamma G_{t+1}^\lambda - \lambda\gamma \hat{v}(S_{t+1}, \textbf{w}) \\
&= \delta_t + \lambda\gamma \big[G_{t+1}^\lambda - \hat{v}(S_{t+1}, \textbf{w})\big] \\
&= \delta_t + \lambda\gamma \delta_{t+1} + (\lambda\gamma)^2 \big[G_{t+2}^\lambda - \hat{v}(S_{t+2}, \textbf{w})\big] \\
&= \delta_t + \lambda\gamma \delta_{t+1} + (\lambda\gamma)^2 \delta_{t+2} + \dots + (\lambda\gamma)^{T-t-2} \delta_{T-2} + (\lambda\gamma)^{T-t-1} \big[G_{T-1}^\lambda - \hat{v}(S_{T-1}, \textbf{w})\big] \\
&= \delta_t + \lambda\gamma \delta_{t+1} + (\lambda\gamma)^2 \delta_{t+2} + \dots + (\lambda\gamma)^{T-t-2} \delta_{T-2} + (\lambda\gamma)^{T-t-1} \big[R_T - \hat{v}(S_{T-1}, \textbf{w})\big] \\
&= \sum_{k=t}^{T-1} (\lambda\gamma)^{k-t} \delta_k
\end{aligned}
$$

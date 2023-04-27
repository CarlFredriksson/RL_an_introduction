# Exercises - Chapter 11

Carl Fredriksson, c@msp.se

## Exercise 11.1

Convert the equation of $n$-step off-policy TD (7.9) to semi-gradient form. Give accompanying definitions of the return for both the episodic and continuing cases.

**My answer:**

$$
\begin{aligned}
\textbf{w}_{t+n} \overset{.}{=} \textbf{w}_{t+n-1} + \alpha \rho_{t:t+n-1} \big[G_{t:t+n} - \hat{v}(S_t,\textbf{w}_{t+n-1})\big] \nabla \hat{v}(S_t,\textbf{w}_{t+n-1})
\end{aligned}
$$

If episodic: $\rho_k = 1$ for all $k \geq T$ (where $T$ is the last step of the episode).

Episodic return:

$$
\begin{aligned}
G_{t:t+n} \overset{.}{=} R_{t+1} + \dots + \gamma^{n-1} R_{t+n} + \gamma^n \hat{v}(S_{t+n},\textbf{w}_{t+n-1})
\end{aligned}
$$

with $G_{t:t+n} = G_t$ if $t+n \geq T$.

Continuing return:

$$
\begin{aligned}
G_{t:t+n} \overset{.}{=} R_{t+1} - \={R}_t + \dots + R_{t+n} - \={R}_{t+n-1} + \hat{v}(S_{t+n},\textbf{w}_{t+n-1})
\end{aligned}
$$

## Exercise 11.2

Convert the equations of $n$-step $Q(\sigma)$ (7.11 and 7.17) to semi-gradient form. Give definitions that cover both the episodic and continuing cases.

**My answer:**

From section 7.6:

>Then we use the earlier update for $n$-step Sarsa without importance-sampling ratios (7.5) instead of (7.11), because now the ratios are incorporated in the $n$-step return.

I believe the exercise description is wrong and it should be (7.5 and 7.17) rather than (7.11 and 7.17). Let $h=t+n$, we have

$$
\begin{aligned}
\textbf{w}_h \overset{.}{=} \textbf{w}_{h-1} + \alpha \big[G_{t:h} - \hat{q}(S_t,A_t,\textbf{w}_{h-1})\big] \nabla \hat{q}(S_t,A_t,\textbf{w}_{h-1})
\end{aligned}
$$

If episodic: $\rho_k = 1$ for all $k \geq T$ (where $T$ is the last step of the episode).

Episodic return:

$$
\begin{aligned}
G_{t:h} \overset{.}{=} R_{t+1} + \gamma \bigg(\sigma_{t+1}\rho_{t+1} + (1-\sigma_{t+1}) \pi(A_{t+1}|S_{t+1}) \bigg) \bigg(G_{t+1:h} - \hat{q}(S_{t+1},A_{t+1},\textbf{w}_{h-1}) \bigg) + \gamma \sum_a \pi(a|S_{t+1}) \hat{q}(S_{t+1},a,\textbf{w}_{h-1})
\end{aligned}
$$

for $t < h \leq T$. The recursion ends with $G_{h:h} \overset{.}{=} \hat{q}(S_h,A_h,\textbf{w}_{h-1})$ if $h<T$, or with $G_{T-1:T} \overset{.}{=} R_T$ if $h=T$.

Continuing return:

$$
\begin{aligned}
G_{t:h} \overset{.}{=} R_{t+1} - \={R}_t + \bigg(\sigma_{t+1}\rho_{t+1} + (1-\sigma_{t+1}) \pi(A_{t+1}|S_{t+1}) \bigg) \bigg(G_{t+1:h} - \hat{q}(S_{t+1},A_{t+1},\textbf{w}_{h-1}) \bigg) + \sum_a \pi(a|S_{t+1}) \hat{q}(S_{t+1},a,\textbf{w}_{h-1})
\end{aligned}
$$

The recursion ends with $G_{h:h} \overset{.}{=} \hat{q}(S_h,A_h,\textbf{w}_{h-1})$.

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

Return episodic:

$$
\begin{aligned}
G_{t:t+n} \overset{.}{=} R_{t+1} + \dots + \gamma^{n-1} R_{t+n} + \gamma^n \hat{v}(S_{t+n},\textbf{w}_{t+n-1})
\end{aligned}
$$

with $G_{t:t+n} = G_t$ if $t+n \geq T$.

Return continuing:

$$
\begin{aligned}
G_{t:t+n} \overset{.}{=} R_{t+1} - \={R}_t + \dots + R_{t+n} - \={R}_{t+n-1} + \hat{v}(S_{t+n},\textbf{w}_{t+n-1})
\end{aligned}
$$

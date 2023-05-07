# Exercises - Chapter 12

Carl Fredriksson, c@msp.se

## Exercise 12.1

Just as the return can be written recursively in terms of the first reward and itself one-step later (3.9), so can the $\lambda$-return. Derive the analogous recursive relationship from (12.2) and (12.1).

**My answer:**

$$
\begin{aligned}
G_t^\lambda &\overset{.}{=} (1-\lambda) \sum_{n=1}^\infty \lambda^{n-1} G_{t:t+n} \\
&= (1-\lambda) \bigg(G_{t:t+1} + \lambda G_{t:t+2} + \lambda^2 G_{t:t+3} + \dots\bigg) \\
&= (1-\lambda) \bigg(\big[R_{t+1} + \gamma \hat{v}(S_{t+1}, w_t)\big] + \lambda \big[R_{t+1} + \gamma R_{t+2} + \gamma^2 \hat{v}(S_{t+2}, w_{t+1})\big] + \lambda^2 \big[R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \gamma^3 \hat{v}(S_{t+3}, w_{t+2})\big] + \dots\bigg) \\
&= (1-\lambda) R_{t+1} \bigg(\sum_{n=0}^\infty \gamma^n\bigg) + (1-\lambda) \gamma \hat{v}(S_{t+1}, w_t) + (1-\lambda) \bigg(\lambda\big[\gamma R_{t+2} + \gamma^2 \hat{v}(S_{t+2}, w_{t+1})\big] + \lambda^2 \big[\gamma R_{t+2} + \gamma^2 R_{t+3} + \gamma^3 \hat{v}(S_{t+3}, w_{t+2})\big] + \dots\bigg) \\
&= \frac{(1-\lambda)}{(1-\lambda)} R_{t+1} + (1-\lambda) \gamma \hat{v}(S_{t+1}, w_t) + (1-\lambda)\lambda\gamma \bigg(\big[R_{t+2} + \gamma \hat{v}(S_{t+2}, w_{t+1})\big] + \lambda \big[R_{t+2} + \gamma R_{t+3} + \gamma^2 \hat{v}(S_{t+3}, w_{t+2})\big] + \dots\bigg) \\
&= R_{t+1} + (1-\lambda) \gamma \hat{v}(S_{t+1}, w_t) + \lambda\gamma(1-\lambda) \sum_{n=1}^\infty \lambda^{n-1} G_{t+1:t+1+n} \\
&= R_{t+1} + (1-\lambda) \gamma \hat{v}(S_{t+1}, w_t) + \lambda\gamma G_{t+1}^\lambda
\end{aligned}
$$

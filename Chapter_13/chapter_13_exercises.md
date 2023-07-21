# Exercises - Chapter 13

Carl Fredriksson, c@msp.se

## Exercise 13.1

Use your knowledge of the gridworld and its dynamics to determine an exact symbolic expression for the optimal probability of selecting the **right** action in Example 13.1.

**My answer:**

Let $A$ denote the second state and $B$ the third state ($S$ is the starting state). We can use the Bellman equation for state values

$$
v_\pi(s) = \sum_{a} \pi(a|s) \sum_{s^\prime,r} p(s^\prime, r|s,a) \big[r + \gamma v_\pi(s^\prime)\big] \text{,} \quad \text{for all} \quad s\in\mathcal{S}
$$

to set up a system of equations

$$
\begin{cases}
v_\pi(S) = \pi(right) \big[-1 + v_\pi(A)\big] + \pi(left) \big[-1 + v_\pi(S)\big] \\
v_\pi(A) = \pi(right) \big[-1 + v_\pi(S)\big] + \pi(left) \big[-1 + v_\pi(B)\big] \\
v_\pi(S) = \pi(right) \big[-1\big] + \pi(left) \big[-1 + v_\pi(A)\big]
\end{cases}
$$

Let $p=\pi(right)$ and note that $\pi(left) = 1-p$, we can rewrite the equations as

$$
\begin{cases}
v_\pi(S) = p \big[-1 + v_\pi(A)\big] + (1-p) \big[-1 + v_\pi(S)\big] \\
v_\pi(A) = p\big[-1 + v_\pi(S)\big] + (1-p) \big[-1 + v_\pi(B)\big] \\
v_\pi(S) = p \big[-1\big] + (1-p) \big[-1 + v_\pi(A)\big]
\end{cases}
$$

$$
\begin{cases}
v_\pi(S) = -1 + p v_\pi(A) + (1-p) v_\pi(S) \\
v_\pi(A) = -1 + p v_\pi(S) + (1-p) v_\pi(B) \\
v_\pi(S) = -1 + (1-p) v_\pi(A)
\end{cases}
$$

The system can be solved to get

$$
v_\pi(S) = -2 \frac{2-p}{p(1-p)}
$$

Our goal is to compute $\argmax_p{\{v_\pi(S) \; | \;0<p<1\}}$ ($p$ is a probability and both $p=0$ and $p=1$ means that the agent will never get to the goal state from the starting state). First we find all critical points, i.e. where the derivative is either zero or doesn't exist.

$$
\frac{\delta v_\pi(S)}{\delta p} = -2 \frac{p(1-p)(-1) - (2-p)(1-2p)}{p^2(1-p)^2}
$$

The derivative doesn't exist for $p=0$ or $p=1$, but since neither critical point satisfies $0<p<1$, we can disregard them. That leaves us with the points where the derivative is zero.

$$
\frac{\delta v_\pi(S)}{\delta p} = 0 \implies p(1-p)(-1) = (2-p)(1-2p)
$$

This equation can be solved to get

$$
p = 2 \plusmn \sqrt{2}
$$

Only $p=2-\sqrt{2} \approx 0.5858$ satisfies $0<p<1$, which means that we have found our optimal probability $p$ of selecting the **right** action. We can use this probability to check that we get the same value for the start state as given in example 13.1

$$
v_\pi(S) = -2 \frac{2-p}{p(1-p)} = -2 \frac{2-(2-\sqrt{2})}{(2-\sqrt{2})(1-(2-\sqrt{2}))} = -6 - 4 \sqrt{2} \approx 11.66
$$

## Exercise 13.2

Generalize the box on page 199, the policy gradient theorem (13.5), the proof of the policy gradient theorem (page 325), and the steps leading to the REINFORCE update equation (13.8), so that (13.8) ends up with a factor of $\gamma^t$ and thus aligns with the general algorithm given in the pseudocode.

**My answer:**

This exercise was tough for me. I asked this question about it: https://ai.stackexchange.com/questions/40894/gammat-in-reinforce-update-sutton-barto-rl-book-exercise-13-2 (no response at the time of writing this).

**Generalize box on 199**

As explained in the box on 199, include a factor of $\gamma$  in the second term of (9.2):

$$
\eta_\gamma(s) = h(s) + \gamma \sum_{\overline{s}} \eta(\overline{s}) \sum_a \pi(a|\overline{s}) p(s|\overline{s},a)
$$

$$
\mu_\gamma(s) = \frac{\eta_\gamma(s)}{\sum_{s^\prime} \eta(s^\prime)}
$$

I initially thought the definition of $\mu_\gamma(s)$ was

$$
\mu_\gamma(s) = \frac{\eta_\gamma(s)}{\sum_{s^\prime} \eta_\gamma(s^\prime)}
$$

but I could not see how to finish the exercise with this definition. Given that we are assuming a single starting state $s_0$, we can also write $\eta_\gamma(s)$ as:

$$
\eta_\gamma(s) = \sum_{k=0}^\infty \gamma^k Pr(s_0 \rightarrow s, k, \pi)
$$

**Generalize Proof of the Policy Gradient Theorem (episodic case)**

I followed the steps in the proof on page 325 and added discounting.

$$
\begin{aligned}
\nabla v_\pi(s) &= \nabla \bigg[\sum_a \pi(a|s) q_\pi(s,a)\bigg] \text{,} \quad \text{for all} \; s \in \mathcal{S} \\
&= \sum_a \bigg[\nabla \pi(a|s) q_\pi(s,a) + \pi(a|s) \nabla q_\pi(s,a)\bigg] \\
&= \sum_a \bigg[\nabla \pi(a|s) q_\pi(s,a) + \pi(a|s) \nabla \sum_{s^\prime,r} p(s^\prime,r|s,a) (r + \gamma v_\pi(s^\prime))\bigg] \\
&= \sum_a \bigg[\nabla \pi(a|s) q_\pi(s,a) + \gamma \pi(a|s) \sum_{s^\prime} p(s^\prime|s,a) \nabla v_\pi(s^\prime)\bigg] \\
&= \sum_a \bigg[\nabla \pi(a|s) q_\pi(s,a) + \gamma \pi(a|s) \sum_{s^\prime} p(s^\prime|s,a) \sum_{a^\prime} \big[\nabla \pi(a^\prime|s^\prime) q_\pi(s^\prime,a^\prime) + \gamma \pi(a^\prime|s^\prime) \sum_{s^{\prime\prime}} p(s^{\prime\prime}|s^\prime,a^\prime) \nabla v_\pi(s^{\prime\prime})\big]\bigg] \\
&= \sum_{x \in \mathcal{S}} \sum_{k=0}^\infty \gamma^k Pr(s \rightarrow x, k, \pi) \sum_a \nabla \pi(a|x) q_\pi(x,a)
\end{aligned}
$$

$$
\begin{aligned}
\nabla J(\theta) &= \nabla v_\pi(s_0) \\
&= \sum_s \bigg(\sum_{k=0}^\infty \gamma^k Pr(s_0 \rightarrow s, k, \pi)\bigg) \sum_a \nabla \pi(a|s) q_\pi(s,a) \\
&= \sum_s \eta_\gamma(s) \sum_a \nabla \pi(a|s) q_\pi(s,a) \\
&= \sum_{s^\prime} \eta(s^\prime) \sum_s \frac{\eta_\gamma(s)}{\sum_{s^\prime} \eta(s^\prime)} \sum_a \nabla \pi(a|s) q_\pi(s,a) \\
&= \sum_{s^\prime} \eta_\gamma(s^\prime) \sum_s \mu_\gamma(s) \sum_a \nabla \pi(a|s) q_\pi(s,a) \\
&\propto \sum_s \mu_\gamma(s) \sum_a \nabla \pi(a|s) q_\pi(s,a)
\end{aligned}
$$

**Steps leading to the REINFORCE update equation (13.8)**

$$
\begin{aligned}
\nabla J(\boldsymbol{\theta}) &\propto \sum_s \mu_\gamma(s) \sum_a q_\pi(s,a,\boldsymbol{\theta}) \nabla \pi(a|s) \\
&= \mathbb{E}_\pi\bigg[\gamma^t \sum_a \pi(a|S_t,\boldsymbol{\theta}) q_\pi(S_t,a) \frac{\nabla \pi(a|S_t,\boldsymbol{\theta})}{\pi(a|S_t,\boldsymbol{\theta})}\bigg] \\
&= \mathbb{E}_\pi\bigg[\gamma^t q_\pi(S_t,A_t) \frac{\nabla \pi(A_t|S_t,\boldsymbol{\theta})}{\pi(A_t|S_t,\boldsymbol{\theta})}\bigg] \\
&= \mathbb{E}_\pi\bigg[\gamma^t G_t \frac{\nabla \pi(A_t|S_t,\boldsymbol{\theta})}{\pi(A_t|S_t,\boldsymbol{\theta})}\bigg]
\end{aligned}
$$

Discounted REINFORCE update:

$$
\begin{aligned}
\boldsymbol{\theta}_{t+1} &\overset{.}{=} \boldsymbol{\theta}_t + \alpha \gamma^t G_t \frac{\nabla \pi(A_t|S_t,\boldsymbol{\theta})}{\pi(A_t|S_t,\boldsymbol{\theta})} \\
&= \boldsymbol{\theta}_t + \alpha \gamma^t G_t \nabla \ln\pi(A_t|S_t,\boldsymbol{\theta})
\end{aligned}
$$

## Exercise 13.3

In Section 13.1 we considered policy parameterizations using the soft-max in action preferences (13.2) with linear action preferences (13.3). For this parameterization, prove that the eligibility vector is

$$
\nabla \ln \pi(a|s,\bm{\theta}) = \textbf{x}(s,a) - \sum_b \pi(b|s,\bm{\theta}) \textbf{x}(s,b)
$$

using the definitions and elementary calculus.

**My answer:**

We have

$$
\pi(a|s,\bm{\theta}) = \frac{e^{h(s,a,\bm{\theta})}}{\sum_b e^{h(s,b,\bm{\theta})}}
$$

with

$$
h(s,a,\bm{\theta}) = \bm{\theta}^\top \textbf{x}(s,a)
$$

Let's start by rewriting the gradient

$$
\begin{aligned}
\nabla \ln \pi(a|s,\bm{\theta}) &= \nabla \ln \bigg(\frac{e^{\bm{\theta}^\top \textbf{x}(s,a)}}{\sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}}\bigg) \\
&= \nabla \bigg(\ln e^{\bm{\theta}^\top \textbf{x}(s,a)} - \ln \sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}\bigg) \\
&= \nabla \ln e^{\bm{\theta}^\top \textbf{x}(s,a)} - \nabla \ln \sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}
\end{aligned}
$$

Let

$$
\frac{\delta}{\delta \bm{\theta}_i}
$$

denote the $i$:th element of $\nabla$. We have

$$
\begin{aligned}
\frac{\delta \ln e^{\bm{\theta}^\top \textbf{x}(s,a)}}{\delta \bm{\theta}_i} &= \frac{\delta \ln e^{\bm{\theta}^\top \textbf{x}(s,a)}}{\delta e^{\bm{\theta}^\top \textbf{x}(s,a)}} \frac{\delta e^{\bm{\theta}^\top \textbf{x}(s,a)}}{\delta \bm{\theta}_i} \\
&= \frac{1}{e^{\bm{\theta}^\top \textbf{x}(s,a)}} \frac{\delta e^{\bm{\theta}^\top \textbf{x}(s,a)}}{\delta \bm{\theta}^\top \textbf{x}(s,a)} \frac{\delta \bm{\theta}^\top \textbf{x}(s,a)}{\delta \bm{\theta}_i} \\
&= \frac{1}{e^{\bm{\theta}^\top \textbf{x}(s,a)}} e^{\bm{\theta}^\top \textbf{x}(s,a)} \textbf{x}(s,a)_i \\
&= \textbf{x}(s,a)_i
\end{aligned}
$$

$$
\begin{aligned}
\frac{\delta \ln \sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}}{\delta \bm{\theta}_i} &= \frac{\delta \ln \sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}}{\delta \sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}} \frac{\delta \sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}}{\delta \bm{\theta}_i} \\
&= \frac{1}{\sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}} \sum_b \frac{\delta e^{\bm{\theta}^\top \textbf{x}(s,b)}}{\delta \bm{\theta}_i} \\
&= \frac{1}{\sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}} \sum_b \frac{\delta e^{\bm{\theta}^\top \textbf{x}(s,b)}}{\delta \bm{\theta}^\top \textbf{x}(s,b)} \frac{\delta \bm{\theta}^\top \textbf{x}(s,b)}{\delta \bm{\theta}_i} \\
&= \frac{1}{\sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}} \sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)} \textbf{x}(s,b)_i \\
&= \sum_b \frac{e^{\bm{\theta}^\top \textbf{x}(s,b)}}{\sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)}} \textbf{x}(s,b)_i \\
&= \sum_b \pi(b|s,\bm{\theta}) \textbf{x}(s,b)_i
\end{aligned}
$$

We can put the pieces together and finish the proof

$$
\begin{aligned}
\nabla \ln \pi(a|s,\bm{\theta}) &= \nabla \ln e^{\bm{\theta}^\top \textbf{x}(s,a)} - \nabla \ln \sum_b e^{\bm{\theta}^\top \textbf{x}(s,b)} \\
&= \textbf{x}(s,a) - \sum_b \pi(b|s,\bm{\theta}) \textbf{x}(s,b)
\end{aligned}
$$

## Exercise 13.4

Show that for the Gaussian policy parameterization (Equations 13.19 and 13.20) the eligibility vector has the following two parts:

$$
\nabla \ln \pi(a|s,\bm{\theta}_\mu) = \frac{\nabla \pi(a|s,\bm{\theta}_\mu)}{\pi(a|s,\bm{\theta})} = \frac{1}{\sigma(s,\bm{\theta})^2} \big(a-\mu(s,\bm{\theta})\big) \textbf{x}_\mu(s)\text{, and}
$$

$$
\nabla \ln \pi(a|s,\bm{\theta}_\sigma) = \frac{\nabla \pi(a|s,\bm{\theta}_\sigma)}{\pi(a|s,\bm{\theta})} = \bigg(\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{\sigma(s,\bm{\theta})^2} - 1\bigg) \textbf{x}_\sigma(s)
$$

**My answer:**

Let

$$
\frac{\delta}{\delta \bm{\theta}_{\mu,i}}
$$

denote the $i$:th element of $\nabla_{\bm{\theta}_\mu}$, and 

$$
\frac{\delta}{\delta \bm{\theta}_{\sigma,i}}
$$

 the $i$:th element of $\nabla_{\bm{\theta}_\sigma}$.
 
Proof for the first part:

$$
\begin{aligned}
\frac{\frac{\delta}{\delta \bm{\theta}_{\mu,i}} \pi(a|s,\bm{\theta}_\mu)}{\pi(a|s,\bm{\theta})} &= \frac{1}{\pi(a|s,\bm{\theta})} \frac{\delta}{\delta \bm{\theta}_{\mu,i}} \bigg[\frac{1}{\sigma(s,\bm{\theta})\sqrt{2}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}\bigg] \\
&= \frac{1}{\pi(a|s,\bm{\theta})} \bigg[\frac{\delta}{\delta \bm{\theta}_{\mu,i}} \bigg(\frac{1}{\sigma(s,\bm{\theta})\sqrt{2}}\bigg) \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} + \frac{1}{\sigma(s,\bm{\theta})\sqrt{2}} \frac{\delta}{\delta \bm{\theta}_{\mu,i}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}\bigg] \\
&= \frac{1}{\pi(a|s,\bm{\theta})} \bigg[\frac{1}{\sigma(s,\bm{\theta})\sqrt{2}} \frac{\delta}{\delta \bm{\theta}_{\mu,i}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}\bigg] \\
&= \frac{1}{\pi(a|s,\bm{\theta}) \sigma(s,\bm{\theta})\sqrt{2}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} \frac{\delta}{\delta \bm{\theta}_{\mu,i}} \bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg) \\
&= \frac{1}{\pi(a|s,\bm{\theta}) \sigma(s,\bm{\theta})\sqrt{2}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} \frac{-1}{2} \bigg(\frac{\sigma(s,\bm{\theta})^2 \frac{\delta}{\delta \bm{\theta}_{\mu,i}} \big(a-\mu(s,\bm{\theta})\big)^2 + \big(a-\mu(s,\bm{\theta})\big)^2 \frac{\delta}{\delta \bm{\theta}_{\mu,i}} \sigma(s,\bm{\theta})^2}{\sigma(s,\bm{\theta})^4}\bigg) \\
&= \frac{1}{\pi(a|s,\bm{\theta}) \sigma(s,\bm{\theta})\sqrt{2}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} \frac{-1}{2} \frac{-2\big(a-\mu(s,\bm{\theta})\big) \frac{\delta}{\delta \bm{\theta}_{\mu,i}} \mu(s,\bm{\theta})}{\sigma(s,\bm{\theta})^2} \\
&= \frac{1}{\pi(a|s,\bm{\theta}) \sigma(s,\bm{\theta})\sqrt{2}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} \frac{\big(a-\mu(s,\bm{\theta})\big) \textbf{x}_\mu(s)_i}{\sigma(s,\bm{\theta})^2} \\
&= \frac{1}{\bigg(\frac{1}{\sigma(s,\bm{\theta})\sqrt{2}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}\bigg) \sigma(s,\bm{\theta})\sqrt{2}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} \frac{\big(a-\mu(s,\bm{\theta})\big) \textbf{x}_\mu(s)_i}{\sigma(s,\bm{\theta})^2} \\
&= \frac{1}{\sigma(s,\bm{\theta})^2} \big(a-\mu(s,\bm{\theta})\big) \textbf{x}_\mu(s)_i
\end{aligned}
$$

$$
\implies \nabla \ln \pi(a|s,\bm{\theta}_\mu) = \frac{\nabla \pi(a|s,\bm{\theta}_\mu)}{\pi(a|s,\bm{\theta})} = \frac{1}{\sigma(s,\bm{\theta})^2} \big(a-\mu(s,\bm{\theta})\big) \textbf{x}_\mu(s)
$$

Proof for the second part:

$$
\begin{aligned}
\frac{\frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \pi(a|s,\bm{\theta}_\sigma)}{\pi(a|s,\bm{\theta})} &= \frac{1}{\pi(a|s,\bm{\theta})} \frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \bigg[\frac{1}{\sigma(s,\bm{\theta})\sqrt{2}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}\bigg] \\
&= \frac{1}{\pi(a|s,\bm{\theta})} \bigg[\frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \bigg(\frac{1}{\sigma(s,\bm{\theta})\sqrt{2}}\bigg) \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} + \frac{1}{\sigma(s,\bm{\theta})\sqrt{2}} \frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}\bigg] \\
&= \frac{1}{\pi(a|s,\bm{\theta})} \bigg[\frac{-\exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}}{\sigma(s,\bm{\theta})^2 \sqrt{2}} \textbf{x}_\sigma(s)_i + \frac{\exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}}{\sigma(s,\bm{\theta})\sqrt{2}} \frac{\big(a-\mu(s,\bm{\theta})\big)^2}{\sigma(s,\bm{\theta})^2} \textbf{x}_\sigma(s)_i\bigg] \\
&= \frac{1}{\bigg(\frac{1}{\sigma(s,\bm{\theta})\sqrt{2}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}\bigg)} \bigg[\frac{-\exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}}{\sigma(s,\bm{\theta})^2 \sqrt{2}} + \frac{\exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)}}{\sigma(s,\bm{\theta})\sqrt{2}} \frac{\big(a-\mu(s,\bm{\theta})\big)^2}{\sigma(s,\bm{\theta})^2}\bigg] \textbf{x}_\sigma(s)_i \\
&= \bigg(\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{\sigma(s,\bm{\theta})^2} - 1\bigg) \textbf{x}_\sigma(s)_i 
\end{aligned}
$$

$$
\implies \nabla \ln \pi(a|s,\bm{\theta}_\sigma) = \frac{\nabla \pi(a|s,\bm{\theta}_\sigma)}{\pi(a|s,\bm{\theta})} = \bigg(\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{\sigma(s,\bm{\theta})^2} - 1\bigg) \textbf{x}_\sigma(s)
$$

Here are the steps for computing the derivates in the second equality:

$$
\begin{aligned}
\frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \frac{1}{\sigma(s,\bm{\theta})\sqrt{2}} &= \frac{1}{\sqrt{2}} \frac{-1}{\sigma(s,\bm{\theta})^2} \frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \sigma(s,\bm{\theta}) \\
&= \frac{-1}{\sigma(s,\bm{\theta})^2 \sqrt{2}} \textbf{x}_\sigma(s)_i
\end{aligned}
$$

and

$$
\begin{aligned}
\frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} &= \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} \frac{-1}{2} \frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \frac{\big(a-\mu(s,\bm{\theta})\big)^2}{\sigma(s,\bm{\theta})^2} \\
&= \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} \frac{-1}{2} \frac{\sigma(s,\bm{\theta})^2 \frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \big(a-\mu(s,\bm{\theta})\big)^2 - \big(a-\mu(s,\bm{\theta})\big)^2 \frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \sigma(s,\bm{\theta})^2}{\sigma(s,\bm{\theta})^4} \\
&= \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} \frac{\big(a-\mu(s,\bm{\theta})\big)^2 \sigma(s,\bm{\theta}) \frac{\delta}{\delta \bm{\theta}_{\sigma,i}} \sigma(s,\bm{\theta})}{\sigma(s,\bm{\theta})^4} \\
&= \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} \frac{\big(a-\mu(s,\bm{\theta})\big)^2 \sigma(s,\bm{\theta})^2 \textbf{x}_\sigma(s)_i}{\sigma(s,\bm{\theta})^4} \\
&= \exp{\bigg(-\frac{\big(a-\mu(s,\bm{\theta})\big)^2}{2\sigma(s,\bm{\theta})^2}\bigg)} \frac{\big(a-\mu(s,\bm{\theta})\big)^2}{\sigma(s,\bm{\theta})^2} \textbf{x}_\sigma(s)_i \\
\end{aligned}
$$
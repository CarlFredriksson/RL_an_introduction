# Exercises - Chapter 9

Carl Fredriksson, c@msp.se

## Exercise 9.1

Show that tabular methods such as presented in Part I of this book are a special case of linear function approximation. What would the feature vectors be?

**My answer:**

The general SGD update for linear function approximation:

$$
\textbf{w}_{t+1} \overset{.}{=} \textbf{w}_t + \alpha \bigg[U_t - \hat{v}(S_t,\textbf{w}_t)\bigg] \textbf{x}(S_t)
$$

We can take state aggregation to the extreme, with one estimated value (one component of the weight vector $\textbf{w}$) for each state: $\textbf{w}_i = V(s_i)$. The feature vectors would also have one element per state, with $\textbf{x}(s_i)$ being a one-hot vector with a 1 at component $i$ and 0 everywhere else. We have 

$$
\hat{v}(S_t,\textbf{w}_t) = \textbf{w}_t^\top \textbf{x} = V(S_t)
$$

and thus the update becomes

$$
V(S_t) \leftarrow V(S_t) + \alpha \bigg[U_t - V(S_t)\bigg]
$$

which is the general form of the update for tabular methods.

## Exercise 9.2

Why does (9.17) define $(n + 1)^k$ distinct features for dimension $k$?

**My answer:**

$n=0, k=1: (s_1^0) = (1)$

$n=1, k=1: (s_1^0, s_1^1) = (1, s_1)$

$n=2, k=1: (s_1^0, s_1^1, s_1^2) = (1, s_1, s_1^2)$

$n=0, k=2: (s_1^0 s_2^0) = (1)$

$n=1, k=2: (s_1^0 s_2^0, s_1^0 s_2^1, s_1^1 s_2^0, s_1^1 s_2^1) = (1, s_2, s_1, s_1 s_2)$

$n=2, k=2: (s_1^0 s_2^0, s_1^0 s_2^1, s_1^0 s_2^2, s_1^1 s_2^0, s_1^1 s_2^1, s_1^1 s_2^2, s_1^2 s_2^0, s_1^2 s_2^1, s_1^2 s_2^2) = (1, s_2, s_2^2, s_1, s_1 s_2, s_1 s_2^2, s_1^2, s_1^2 s_2, s_1^2 s_2^2)$

We have $k$ numbers $s_i$ that all have $n+1$ possible exponents $0,1,\dots,n$. Combining all of the numbers and possible exponents we get $(n+1)^k$ permutations.

## Exercise 9.3

What $n$ and $c_{i,j}$ produce the feature vectors $\textbf{x}(s) = (1, s_1, s_2, s_1 s_2, s_1^2, s_2^2, s_1 s_2^2, s_1^2 s_2, s_1^2 s_2^2)^\top$

**My answer:**

$n=2, k=2$

$c_{0,1}=0, c_{0,2}=0, c_{1,1}=1, c_{1,2}=0, c_{2,1}=0, c_{2,2}=1, c_{3,1}=1, c_{3,2}=1, c_{4,1}=2, c_{4,2}=0, c_{5,1}=0, c_{5,2}=2, c_{6,1}=1, c_{6,2}=2, c_{7,1}=2, c_{7,2}=1, c_{8,1}=2, c_{8,2}=2$

Gives us

$x_0(s) = \prod_{j=1}^k s_j^{c_{i,j}} = s_1^{c_{0,1}} s_2^{c_{0,2}} = s_1^0 s_2^0 = 1$

$x_1(s) = s_1^{c_{1,1}} s_2^{c_{1,2}} = s_1^1 s_2^0 = s_1$

$x_2(s) = s_1^{c_{2,1}} s_2^{c_{2,2}} = s_1^0 s_2^1 = s_2$

$x_3(s) = s_1^{c_{3,1}} s_2^{c_{3,2}} = s_1^1 s_2^1 = s_1 s_2$

$x_4(s) = s_1^{c_{4,1}} s_2^{c_{4,2}} = s_1^2 s_2^0 = s_1^2$

$x_5(s) = s_1^{c_{5,1}} s_2^{c_{5,2}} = s_1^0 s_2^2 = s_2^2$

$x_6(s) = s_1^{c_{6,1}} s_2^{c_{6,2}} = s_1^1 s_2^2 = s_1 s_2^2$

$x_7(s) = s_1^{c_{7,1}} s_2^{c_{7,2}} = s_1^2 s_2^1 = s_1^2 s_2$

$x_8(s) = s_1^{c_{8,1}} s_2^{c_{8,2}} = s_1^2 s_2^2 = s_1^2 s_2^2$

$\implies \textbf{x}(s) = (1, s_1, s_2, s_1 s_2, s_1^2, s_2^2, s_1 s_2^2, s_1^2 s_2, s_1^2 s_2^2)$

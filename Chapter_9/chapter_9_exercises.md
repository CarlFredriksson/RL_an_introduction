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

# Exercises - Chapter 5

Carl Fredriksson, c@msp.se

## Exercise 5.1

Consider the diagrams on the right in Figure 5.1. Why does the estimated value function jump up for the last two rows in the rear? Why does it drop off for the whole last row on the left? Why are the frontmost values higher in the upper diagrams than in the lower?

**My answer:**

It jumps up for the last two rows in the rear since for any other player sum the player hits and is likely to end up going bust. Additionally, 20 or 21 will often be better than what the dealer gets (and the dealer can go bust).

It drops off for the whole last row on the left since the dealer is showing an ace, which is the best first card and thus reduces the likelihood that the player wins. An ace combines with one or two 10-valued cards, which is the most common card value, to make 21, and it's flexible.

The frontmost values are higher in the upper diagrams because the player is holding a usable ace and is thus less likely to bust and more likely to get to 20 or 21.

## Exercise 5.2

Suppose every-visit MC was used instead of first-visit MC on the blackjack task. Would you expect the results to be very different? Why or why not?

**My answer:**

I would not expect the results to be different at all, since the first-visit to a state will be the only visit to that state during the episode. The same player sum might occur twice, but the first time usable ace will be true and the second time it will be false.

## Exercise 5.3

What is the backup diagram for Monte Carlo estimation of $q_\pi$?

**My answer:**

It's the same as for $v_\pi$, except that the root is a state-action pair. Below the state-action root is the entire trajectory of transitions along a particular single episode, ending at the terminal state.

## Exercise 5.4

The pseudocode for Monte Carlo ES is inefficient because, for each state–action pair, it maintains a list of all returns and repeatedly calculates their mean. It would be more efficient to use techniques similar to those explained in Section 2.4 to maintain just the mean and a count (for each state–action pair) and update them incrementally. Describe how the pseudocode would be altered to achieve this.

**My answer:**

* Remove the returns storage.
* Initialize $N(s, a) \leftarrow 0$, for all $s \in \mathcal{S}$, $a \in \mathcal{A}(s)$.
* Increment $N(s, a)$ every time the the state-action pair $(s, a)$ is visited.
* Change the $Q$-update to:

$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \frac{1}{N(S_t, A_t)} (G - Q(S_t, A_t))
$$

## Exercise 5.5

Consider an MDP with a single nonterminal state and a single action that transitions back to the nonterminal state with probability $p$ and transitions to the terminal state with probability $1 - p$. Let the reward be $+1$ on all transitions, and let $\gamma = 1$. Suppose you observe one episode that lasts 10 steps, with a return of 10. What are the first-visit and every-visit estimators of the value of the nonterminal state?

**My answer:**

Since there is only one action, there is only one possible policy and thus $\rho_{t:T(t)-1} = 1$ for all $t$. This means that there is no difference between the ordinary and weighted importance sampling, since $\sum_{t \in \mathcal{T}(s)} \rho_{t:T(t)-1} = |\mathcal{T}(s)|$.

First-visit:

$$
V(s) = G_0 = 10
$$

Every-visit:

$$
V(s) = \frac{G_0 + G_0 + \dots + G_{9}}{|\mathcal{T}(s)|} = \frac{10 + 9 + \dots + 1}{10} = 10 (\frac{10 + 1}{2}) = 55
$$

## Exercise 5.6

# Exercises - Chapter 8

Carl Fredriksson, c@msp.se

## Exercise 8.1

The non-planning method looks particularly poor in Figure 8.3 because it is a one-step method; a method using multi-step bootstrapping would do better. Do you think one of the multi-step bootstrapping methods from Chapter 7 could do as well as the Dyna method? Explain why or why not.

**My answer:**

If by doing well we refer to finding a complete optimal policy in the least number of episodes, then I don't think the multi-step bootstrapping methods from Chapter 7 could do as well as the Dyna method. With $n=50$ a complete optimal policy is found after 3 episodes, and with larger $n$ the algorithm might do even better. I don't think any of the multi-step bootstrapping methods are likely to find a complete optimal policy in 3 episodes. If we use many steps per update (large $n$ in the $n$-step method sense), maybe even going all the way to Monte-Carlo and using all steps in the episode, we would quickly start doing updates in each state. However, many of these updates will not move the policy efficiently towards optimality. Imagine the chaotic first episode of about 1700 steps and assume that all action-values were initialized to 0 and a large $n$ was used. Many sub-optimal actions were taken in many states, yet many of these will be the new greedy actions after the first episode. If we instead use a small $n$, the starting state and other states to the left in the grid are unlikely to be meaningfully updated in the first few episodes and it seems very unlikely that we find a complete optimal policy in 3 episodes.

If by doing well we instead refer to something like finding a complete optimal policy in the shortest clock time or least number of computer instructions, I think it could be more competitive between Dyna and the multi-step bootstrapping methods.

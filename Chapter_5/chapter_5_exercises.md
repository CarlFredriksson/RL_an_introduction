# Exercises - Chapter 5

Carl Fredriksson, c@msp.se

## Exercise 5.1

Consider the diagrams on the right in Figure 5.1. Why does the estimated value function jump up for the last two rows in the rear? Why does it drop off for the whole last row on the left? Why are the frontmost values higher in the upper diagrams than in the lower?

**My answer:**

It jumps up for the last two rows in the rear since for any other player sum the player hits and is likely end up going bust. Additionally, 20 or 21 will often be better than what the dealer gets (and the dealer can go bust).

It drops off for the whole last row on the left since the dealer is showing an ace, which is the best first card and thus reduces the likelihood that the player wins. An ace combines with one or two 10-valued cards, which is the most common card value, to make 21, and it's flexible.

The frontmost values are higher in the upper diagrams because the player is holding a usable ace and is thus less likely to bust and more likely to get to 20 or 21.

## Exercise 5.2

Suppose every-visit MC was used instead of first-visit MC on the blackjack task. Would you expect the results to be very different? Why or why not?

**My answer:**

I would not expect the results to be different at all since the first-visit to a state will be the only visit to that state during the episode. The same player sum might occur twice, but the first time usable ace will be true and the second time it will be false.

## Exercise 5.3

What is the backup diagram for Monte Carlo estimation of $q_\pi$?

**My answer:**

It's the same as for $v_\pi$, except that the root is an action node (a state-action pair). Below the action node root is the entire trajectory of transitions along a particular single episode, ending at the terminal state.

## Exercise 5.4


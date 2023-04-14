# Exercises - Chapter 10

Carl Fredriksson, c@msp.se

## Exercise 10.1

We have not explicitly considered or given pseudocode for any Monte Carlo methods in this chapter. What would they be like? Why is it reasonable not to give pseudocode for them? How would they perform on the Mountain Car task?

**My answer:**

> What would they be like?

Generate episodes in the same way, but update value estimates only in between episodes using full returns from the previous episode.

> Why is it reasonable not to give pseudocode for them?

Because they are special cases of $n$-step Sarsa (by setting $n$ to be the length of the the episodes).

> How would they perform on the Mountain Car task?

Poorly. The performance seems to be best for intermediate levels of bootstrapping (peaking at $n=4$). Larger $n$ leads to worse performance, and as mentioned above, Monte Carlo (MC) methods are equivalent to the extreme case with the maximum $n$. We can also reason about how the episodes would play out. With MC methods and $\textbf{w}$ initialized to $\textbf{0}$, we would have very long early episodes. Since updates are only made after reaching the terminal state, action selection would be completely random for the entirety of the first episode, which would be incredibly long for the majority of runs.

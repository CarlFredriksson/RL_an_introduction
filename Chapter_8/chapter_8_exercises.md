# Exercises - Chapter 8

Carl Fredriksson, c@msp.se

## Exercise 8.1

The non-planning method looks particularly poor in Figure 8.3 because it is a one-step method; a method using multi-step bootstrapping would do better. Do you think one of the multi-step bootstrapping methods from Chapter 7 could do as well as the Dyna method? Explain why or why not.

**My answer:**

If by doing well we refer to finding a complete optimal policy in the least number of episodes, then I don't think the multi-step bootstrapping methods from Chapter 7 could do as well as the Dyna method. With $n=50$ a complete optimal policy is found after 3 episodes, and with larger $n$ the algorithm might do even better. I don't think any of the multi-step bootstrapping methods are likely to find a complete optimal policy in 3 episodes. If we use many steps per update (large $n$ in the $n$-step method sense), maybe even going all the way to Monte-Carlo and using all steps in the episode, we would quickly start doing updates in each state. However, many of these updates will not move the policy efficiently towards optimality. Imagine the chaotic first episode of about 1700 steps and assume that all action-values were initialized to 0 and a large $n$ was used. Many sub-optimal actions were taken in many states, yet many of these will be the new greedy actions after the first episode. If we instead use a small $n$, the starting state and other states to the left in the grid are unlikely to be meaningfully updated in the first few episodes and it seems very unlikely that we find a complete optimal policy in 3 episodes.

If by doing well we instead refer to something like finding a complete optimal policy in the shortest clock time or least number of computer instructions, I think it could be more competitive between Dyna and the multi-step bootstrapping methods.

## Exercise 8.2

Why did the Dyna agent with exploration bonus, Dyna-Q+, perform better in the first phase as well as in the second phase of the blocking and shortcut experiments?

**My answer:**

The increased exploration made Dyna-Q+ find an optimal policy quicker (while still continuing to explore - which is why line is not completely straight). Less exploration can lead to exploitation of sub-par policies for longer.

## Exercise 8.3

Careful inspection of Figure 8.5 reveals that the difference between Dyna-Q+ and Dyna-Q narrowed slightly over the first part of the experiment. What is the reason for this?

**My answer:**

It took longer for Dyna-Q to find an optimal policy. However, once it was found it exploited that policy to a greater extent than Dyna-Q+, due to less exploration, and started accumulating reward at a slightly faster rate and thus would slowly catch up in cumulative reward. When the environment changed and only Dyna-Q+ found the new faster path, the difference in cumulative reward started growing in the favor of Dyna-Q+.

## Exercise 8.4 (programming)

The exploration bonus described above actually changes the estimated values of states and actions. Is this necessary? Suppose the bonus $\kappa \sqrt{\tau}$ was used not in updates, but solely in action selection. That is, suppose the action selected was always that for which $Q(S_t, a) + \kappa \sqrt{\tau(S_t,a)}$ was maximal. Carry out a gridworld experiment that tests and illustrates the strengths and weaknesses of this alternate approach.

**My answer:**

I used the same shortcut maze problem as in Example 8.3. It seems like the alternate approach to Dyna-Q+ (Dyna-Q+ v2 in the plot), performed better on the problem before the shortcut opened, but worse after. 

Below is a plot where the algorithms were run one time each. It seems like Dyna-Q+ v2 started to find the shortcut slower than Dyna-Q+ and didn't exploit it as well when found.

![Ex 8.4 Shortcut Maze Result One Run](Exercise_8_4/shortcut_maze_result_one_run.png)

Below is a plot where the cumulative reward was averaged over 10 runs per algorithm. Averaging over multiple runs provides a fairer comparison since performance varies between runs.

![Ex 8.4 Shortcut Maze Result 10 Run Average](Exercise_8_4/shortcut_maze_result_10_run_avg.png)

Note that the methods were highly sensitive to parameter settings and the shown results are simply from one set of parameter settings. Thus I find it hard to make strong statements regarding strengths and weaknesses of the alternative approach to Dyna-Q+.

## Exercise 8.5

How might the tabular Dyna-Q algorithm shown on page 164 be modified to handle stochastic environments? How might this modification perform poorly on changing environments such as considered in this section? How could the algorithm be modified to handle stochastic environments *and* changing environments?

**My answer:**


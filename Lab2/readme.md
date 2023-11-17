# Computational Intelligence Lab 2
The goal of the lab was to implement an evolution strategy (ES) to create an agent able to play Nim game. 

I developed two strategies both with self-adaptation:

*  ( &mu; , &lambda; ) - ES 
*  ( &mu; + &lambda; ) - ES

I have created a list of rules and  assigned to each of them a random weight.

The weights are used as the probability to use that rule in a single move during the game.

This logic is implemented in the **Player** class.

The **fitness** for both algorithms is the **percentage** of wins against the **optimal** strategy.

## ( &mu; , &lambda; ) - ES
This strategy uses self adaptation with a single &sigma; parameter. 

It is modified every 20 steps in according to the 
1/5 rule.

## ( &mu; + &lambda; ) - ES
This strategy uses self adaptation with a vector of &sigma; parameter, one for every element in the parents list.

They are modified according to a gaussian with mean &sigma; and standard deviation equal to 0.2.

## Considerations
* Some rules are not fully deterministic. For this reason the fitness is not fully deterministic too, 
but it is still reliable looking at the results.
* One of the rules is very similar to the optimal one and in a previous analysis it is shown that it can beat often 
the optimal. Given that, we can observe that the final weights of the presumed "best players" generated are imbalanced
in favor of that rule. This can be interpreted as the demonstration that the algorithm converges towards the optimum.
* Self-adaptation makes the algorithm really slow even with the 5 Nim grid used in the code attached.
* After the generation of the best players, the best among them is taken and used to simulate 10_000 games against
the optimal strategy: the percentage of wins is approximately 50% for both algorithms.


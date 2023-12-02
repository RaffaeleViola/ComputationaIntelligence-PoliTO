# Computational Intelligence Lab 2
The goal of the lab was to implement an evolutionary algorithm (EA) able to optimize different black box 
fitness functions. 

I developed 3 strategies:

*  GA algorithm with mutation and crossover mutually exclusive (First Approach)
*  GA algorithm with mutation and crossover applied subsequently (Chosen approach)
*  GA algorithm with island model (Approach for 5 - 10 instances)

All the mechanism implement a **cache** in order to not compute the fitness for already seen individuals.

## First Approach
This approach has a low mutation probability equal to 0.2 and uses uniform crossover. After some experiments uniform 
crossover seems to be the most effective.

## Chosen Approach
This approach gives on average the best results over all the problem instances even though it is mostly effective 
on instances 1 and 2.
It firstly applies mutation over two selected parents (tournament) and after that it applies uniform crossover.
On problems 5 and 10 the algorithm tends to reach a plateau in the fitness landscape, and it is no more able to escape 
from that. The reason is probably that the fitness landscape of that instances has few picks that are hard to find,
also by favoring exploration over exploitation.

## Approach for 5 - 10 instances
This approach implements an island model that is better in finding good solutions, but it needs more fitness calls.
For problems 5 - 10, particularly thanks to the extinction mechanism, it is able to explore more parts of the fitness
landscape and in this way it can find better results than the previous model for these instances.

## Results
* Chosen Approach

  * Instance 1 - fitness: 15129, calls: 1.00
  * Instance 2 - fitness: 55628, calls: 0.956
  * Instance 5 - fitness: 10628, calls: 0.350
  * Instance 10 - fitness: 3129, calls: 0.230


* Approach suitable for 5 - 10

  * Instance 1 - fitness: 90528, calls: 1.00
  * Instance 2 - fitness: 90085, calls: 0.978
  * Instance 5 - fitness: 90124, calls: 0.438
  * Instance 10 - fitness: 90523 calls: 0.408

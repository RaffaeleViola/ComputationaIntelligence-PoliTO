### Raffaele Viola - s309063
### Lab 1

* Implemented A* algorithm with g(n) equal to the length of the set of the current states taken and h(n) equal to the
  number of pieces to cover (problem  size minus the sum of the logical or between all the states taken)
* After professor showed in class that h(n) made like that was not admissible, I focused on optimizing the solution 
  proposed in class. 
* I optimized the last part of the function by reducing the check over the missing size from O(n^2) to O(n).
* I showed the results of the optimization by measuring and printing the running time of the two algorithms.

 ***

### Halloween Challenge
* Implemented standard Hill Climber
* Implemented Simulated Annealing Hill Climber
* Performed memoization in order to reduce the number of fitness calls

 ***

### Lab 2

* I developed two strategies both with self-adaptation:

  *  ( &mu; , &lambda; ) - ES 
  *  ( &mu; + &lambda; ) - ES

* I have created a list of rules and  assigned to each of them a random weight.
The weights are used as the probability to use that rule in a single move during the game.
The **fitness** for both algorithms is the **percentage** of wins against the **optimal** strategy.
#### ( &mu; , &lambda; ) - ES
* This strategy uses self adaptation with a single &sigma; parameter.
It is modified every 20 steps according to the 
1/5 rule.
#### ( &mu; + &lambda; ) - ES
* This strategy uses self adaptation with a vector of &sigma; parameter, one for every element in the parents list.
They are modified according to a gaussian with mean &sigma; and standard deviation equal to 0.2.

* After the generation of the best players, the best among them is taken and used to simulate 10_000 games against
the optimal strategy: the percentage of wins is approximately 50% for both algorithms. The algorithms in general tend to
increase the weight of the rule that performs better used alone (take_even_odd rule), since the other rules are quite 
ineffective against the optimal player. This means that the algorithms converge towards the optimum.

#### Reviews done
* Giulio Figliolino s317510: Suggested that his fitness function could be better designed since he made every offspring player
  playing against each other. Using a fixed deterministic opponent could have helped to measure a more accurate fitness 
  value. I also suggested that 10 generations are a bit low and could not show significant results in this kind of 
  algorithms.
* Luca Solaini s306033: Suggested that there was a minor issue in the self-adaptation strategy in which the statistics collected
  for the 1/5 rule where used in the opposite way (numerator and denominator swapped), leading to not actually self-adapting.
#### Reviews received
* Davide Natale: He said that the code was clear and understandable. He suggested to test the agent also a second player.
No other suggestions.
* Salvatore Latino s314872: He properly analyzed my developed code and stated that it was a good implementation. He 
suggested to implement an ageing strategy. Overall a good suggestion but the results did not change a lot. I think this
happens because the fitness landscape is not problematic (there are no local maximum, only a maximum corresponding to
1.0 for the rule take_even_odd and 0.0. the others). No other suggestions.
* Angelo Iannielli s317887: He suggested to add more comments and print more information. I tried to follow this good tip in
the subsequent labs. He suggested to use a trainer different from the optimal one because this could lead to insert a bias.
In my opinion it is in general true and the best strategy would be to alternate different trainers. However, Nim is a simple
game and I think that using other strategies would have only slowed the convergence, at least considering my specific rule set.

 ***

### Lab 9
* I developed 3 strategies:

  *  GA algorithm with mutation and crossover mutually exclusive
  *  GA algorithm with mutation and crossover applied subsequently (Chosen approach)
  *  GA algorithm with island model (Approach for 5 - 10 instances)

* I have tested different types of crossover and finally chosen the uniform as the more effective.
* Parent selection is performed with Tournament 
* All the mechanisms implement a **cache** in order to not compute the fitness for already seen individuals.
#### Chosen Approach
* This approach gives on average the best results over all the problem instances even though it is mostly effective 
on instances 1 and 2.
#### Approach for 5 - 10 instances
* This approach implements an island model that is better in finding good solutions, but it needs more fitness calls.
For problems 5 - 10, particularly thanks to the extinction mechanism, it is able to explore more parts of the fitness
landscape and in this way it can find better results than the previous model for these instances.
#### Reviews done
* Luca Barbato s320213: Suggested to explore more crossover strategies rather than only one-cut and to save (and reuse) 
  the fitness of already seen individuals to improve the performances.
* Lorenzo Nikiforos s317616: Overall good implementation, I suggested to implement the migration for the island model and
 to store the fitness of already seen individuals.

#### Reviews received
* Alexandro Buffa s316999: He noticed that I missed the line where I upgrade the cache. He was right and I fixed it.
* Luana Pulignano s314156: She appreciated how the code was structured and the strategies adopted. No suggestions to
improve.
* Ludovico Fiorio s306058: He suggested to make the prints more detailed, to mutate more than one bit at a time and to check for 
fitness equal to 1 for an early stop. All good points. The early stop was already implemented by comparing the absolute 
increase of fitness respect to the previous generation with a threshold.

 ***

### Lab 10
* The strategy applied to create the agent able to play TicTacToe is the Q-Learning with Model-Free approach. The reward
system is: +1 for winning game, 0 for draw, -1 for losing game. After every game the reward is backpropagated through 
the history of states/moves (the future state used to upgrade the Qtable is the state after the subsequent move of the
opponent). The agent policy during training is an epsilon greedy policy. 
* The QTable is a hashmap:

  - key -> board state as tuple (hashable in Python)
  - value -> hashmap with key the tuple of the move (action) and value the float associated to that action

The Qtable is initialized to a default value that I have chosen as 0.

* The opponents of the agent are both a Random Player (p = 66,66%) and a MinMax Player (p = 33,34%). By trying with only 
random player I noticed that the agent struggled to learn a reasonable amount of good strategies. I added a MinMax Agent 
to solve this issue, but it is needed to exchange them because the MinMax agent is deterministic and this means that 
against him my agent would learn only few strategies.
* These are the results:
  - Loosing Rate against every player (10_000 games):

|  Agent   | MinMaxPlayer | RandomPlayer | MyPlayer |
|:--------:|:------------:|:------------:|:--------:|
| MyPlayer |     0.0%     |     2.7%     |   0.0%   |


#### Reviews done
* Marco Cirone s314878: The main suggestion was to implement a backpropagation strategy by packing the history of states/moves
rather than upgrading with reward only the previous move.
* Ivan Magistro Contenta s314356: Same previous suggestion and I also suggested to store in qtable only the real available
  actions (not all the nine positions) in order to reduce the memory footprint of the table. 

#### Reviews received
* Salvatore Latino s314872: He complimented for the implementation. Only suggestion was to use "Magic Square" proposed 
in class. Good point, but I had already  considered that and I found myself more comfortable with a standard matrix.
* Nunzio Messineo s315067: He complimented for the implementation but suggested to reorganize the code to make it more
understandable.

 ***

### Quixo Exam

#### MinMax
* Implemented MinMax Strategy with a limited depth considering the large search space 
* Implemented alpha-beta pruning to reduce the branching factor
* Added a cache to speed up the MinMax response and not recompute all the tree at every move (the cache considers also
 the depth)
* Implemented rotations of the table in order to reduce more the branching factor
* Firstly the score system was standard (+1 win, -1 lose, 0 draw) but I noticed 
 that the model was unable to learn something useful in the first stages of the game. I thus implemented a score function
 that consists in the sum of the maximum row, column and diagonal density.

```

def scoring_fun(game: Game, player: int, to_maximize: int):
    brd = game.get_board()
    max_rows = max([(brd[i, :] == player).sum() for i in range(5)])
    max_columns = max([(brd[:, i] == player).sum() for i in range(5)])
    diag1 = sum([(brd[i, i] == player).sum() for i in range(5)])
    diag2 = sum([(brd[i, j] == player).sum() for i, j in zip(range(5), range(4, -1, -1))])
    mapping = {0: 0, 1: 1, 2: 10, 3: 100, 4: 1000, 5: 10_000}
    if player == to_maximize:
        return mapping[max_rows] + mapping[max_columns] + mapping[diag1] + mapping[diag2]
    else:
        return -(mapping[max_rows] + mapping[max_columns] + mapping[diag1] + mapping[diag2])

```

#### QLearning Tentative
* I tried to implement a QLearning approach but even making it training for long time lead me to a quite random strategy.
I left the code on GitHub, but I did not create an agent for the exam because I moved to the evaluation of the MCTS approach, that 
seemed to me more promising for this task. The Qlearning implemented do not use Deep Learning.

#### Montecarlo Tree Search
* I explored and implemented the Montecarlo Tree Search. I implemented a Node class to represent a state generated 
 by a given player (Important because the same state can be generated by both players). 

```
    def __init__(self, board: np.ndarray, player: int, parent=None):
        self.state = board.copy()
        self.player = player  # the player that generated the current board
        self.wins = 0
        self.draws = 0
        self.visits = 0
        self.parent = parent
        tmp_game = Game()
        tmp_game._board = board.copy()
        tmp_game.current_player_idx = player
        self.over = tmp_game.check_winner()
        tmp_game.current_player_idx = (player + 1) % 2
        self.next_moves = next_accetptable_moves(tmp_game, (player + 1) % 2)
        self.childs: dict[Node, Move] = dict()
```

* I apply the Selection - Expansion - Simulation - Backpropagation 100 times and the simulation is performed over 70 games.
* The selection is performed by computing the Upper Confidence Bound (UCB) and then taking the child node with the highest value.
  I found this metric in an article on Medium blog. Selection stops when it reaches a leaf node.

```
      def calculate_ucb(self) -> float:
        if self.visits == 0:
            return math.inf
        parent_node_visits = self.parent.visits
        exploration_term = (math.sqrt(2.0) * math.sqrt(math.log(parent_node_visits) / self.visits))
        value = self.value() + exploration_term
        return value
```

* The expansion is performed by selecting randomly one of the possible moves available from the previously selected node
 and creating the new child node.
* The simulation is performed by playing 70 random games and computing the statistics (win and draw rate)
* The backpropagation is performed by propagating, following the parent pointer in the nodes, the previous statistics.
* Given the fact that the search space is not a tree because some boards can be recreated during the game (there are 
cycles in the tree), I have added a global cache used in the selection phase to start from an already visited state as root
(if present), and a local cache that avoids to get stuck in a cycle while visiting the tree towards a leaf.

#### Agents Fused
* I observed that:
  * MCTS is really slow by construction, and It is not effective in the first stages of the game.
  * MinMax is really effective but conservative, thus in some games his strategy results not really "aggressive" and this 
  may lead to losing the game
* In order to enhance the overall performance I mixed the 2 agents. Most of the time the player is MinMax but if the 
board has few free spots (the strategy is too conservative) or the MinMax plays a move that leads the opponent to 
victory, the move is performed by MCTS. It is important to say that MinMax is depth-limited, thus it may end up in a 
situation where every move leads the opponent to victory (for example the "doppio gioco" as in Tic Tac Toe)

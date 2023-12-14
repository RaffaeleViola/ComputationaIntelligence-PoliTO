# Lab10 - Reinforcement learning applied to TicTacToe

### TicTacToe Implementation

The game is implemented with the class TicTacToe. The board is a 2-D numpy array with these symbols:

- 0 -> empty
- 1 -> X
- -1 -> O

A move corresponds to the tuple of indices of the matrix (ex. (0,0) -> high left corner).

The logic of the class is straightforward.


### Strategy
The strategy applied to create the agent able to play TicTacToe is the Q-Learning with Model-Free approach.

The QTable is a hashmap:

- key -> board state as tuple of tuples (hashable in Python)
- value -> hashmap with key the tuple of the move (action) and value the float associated to that action

The Qtable is initialized to a default value that I have chosen as 0.

The reward is system is:

- +1 for winning game
- 0 for draw
- -1 for losing game

A training episodes corresponds to 2 games, 1 where the agent plays as first and one where it plays as second.

After every game the reward is backpropagated through the history of states. Keep Attention: the future state used to 
compute Bellman equation (upgrade the Qtable) is the state after the subsequent move of the opponent. 
Example:

- empty table *((0, 0, 0), (0, 0, 0), (0, 0, 0))*
- Player X move *(0, 0) -> ((1, 0, 0), (0, 0, 0), (0, 0, 0))*
- Player 0 move *(0, 1) -> ((1, -1, 0), (0, 0, 0), (0, 0, 0))*
- Current State: *((0, 0, 0), (0, 0, 0), (0, 0, 0))* - Current Action: *(0, 0)* - 
Future State: *((1, -1, 0), (0, 0, 0), (0, 0, 0))*

Our agent policy during training is an *epsilon greedy policy*. We have probability = epsilon to choose a random move and
probability = 1 - epsilon to choose the max move in Qtable. Epsilon is degradated every training episode until it reaches 
0.01 .

The opponents of our agent are both a Random Player (p = 66,66%) and a MinMax Player (p = 33,34%). By trying with only 
random player I noticed that the agent struggled to learn a reasonable amount of strategies. I added a MinMax Agent to 
solve this issue, but it is needed to exchange them because the MinMax agent is *deterministic* and this means that
against him our agent would learn only few strategies when epsilon is high (first learning episodes).

### Results
The results are pretty good. The agent perfectly learn to play against MinMaxAgent and it wins or draws more than 90% of
times against a random player. There are a small amount of strategies that it was not able to learn, thus an improvement 
could be a sort of continuous learning during games to adjust this issue. 
  
- Loosing Rate against every player:

| Agent         | MinMaxPlayer | RandomPlayer | PerfectPlayer |
| :---:         | :---:          | :---:          | :---:     |
| PerfectPlayer | 0.0% | 2.7% | 0.0% |




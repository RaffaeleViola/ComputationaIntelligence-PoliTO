import math
import random
from copy import deepcopy
import numpy as np
from game import Player, Move, Game
from quixo_exam.trainingQlearning import next_accetptable_moves, MyRandomPlayer


class MonetCarloGame(Game):

    def __init__(self):
        super().__init__()
        self.last_degree = 0

    def play(self, player1: Player, player2: Player):
        state_history = [tuple(self.get_board().ravel())]
        actions_history = []
        degree_list = []
        players = [player1, player2]
        winner = -1
        steps = 0
        while winner < 0:
            self.current_player_idx += 1
            self.current_player_idx %= len(players)
            ok = False
            while not ok:
                from_pos, slide = players[self.current_player_idx].make_move(
                    self)
                ok = self.move(from_pos, slide, self.current_player_idx)
                if ok:
                    if self.current_player_idx == 0:
                        actions_history.append((from_pos, slide))
                        degree_list.append(self.last_degree)
                    else:
                        state_history.append(tuple(self.get_board().ravel()))
            # self.print()
            steps += 1
            if steps == 100:
                return -1, state_history, actions_history, degree_list
            winner = self.check_winner()
        return winner, state_history, actions_history, degree_list

    @staticmethod
    def simulate_move(state: np.ndarray, move: tuple[tuple[int, int], Move], player_id: int):
        new_g = MonetCarloGame()
        new_g._board = state.copy()
        new_g.current_player_idx = player_id
        ok = new_g.move(move[0], move[1], player_id)
        if not ok:
            print("Unknown Error")
        return new_g.get_board()

    @staticmethod
    def flip_board(state: np.ndarray):
        fun_to_map = np.vectorize(lambda x: (x + 1) % 2 if x in [0, 1] else x)
        cp = state.copy()
        return fun_to_map(cp)

    def move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
        '''Perform a move'''
        if player_id > 2:
            return False
        # Oh God, Numpy arrays
        prev_value = deepcopy(self._board[(from_pos[1], from_pos[0])])
        acceptable = self.take((from_pos[1], from_pos[0]), player_id)
        if acceptable:
            acceptable = self.slide((from_pos[1], from_pos[0]), slide)
            if not acceptable:
                self._board[(from_pos[1], from_pos[0])] = deepcopy(prev_value)
        return acceptable

    def take(self, from_pos: tuple[int, int], player_id: int) -> bool:
        '''Take piece'''
        # acceptable only if in border
        acceptable: bool = (
                               # check if it is in the first row
                                   (from_pos[0] == 0 and from_pos[1] < 5)
                                   # check if it is in the last row
                                   or (from_pos[0] == 4 and from_pos[1] < 5)
                                   # check if it is in the first column
                                   or (from_pos[1] == 0 and from_pos[0] < 5)
                                   # check if it is in the last column
                                   or (from_pos[1] == 4 and from_pos[0] < 5)
                               # and check if the piece can be moved by the current player
                           ) and (self._board[from_pos] < 0 or self._board[from_pos] == player_id)
        if acceptable:
            self._board[from_pos] = player_id
        return acceptable

    def slide(self, from_pos: tuple[int, int], slide: Move) -> bool:
        '''Slide the other pieces'''
        # define the corners
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position is not in a corner
        if from_pos not in SIDES:
            # if it is at the TOP, it can be moved down, left or right
            acceptable_top: bool = from_pos[0] == 0 and (
                    slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is at the BOTTOM, it can be moved up, left or right
            acceptable_bottom: bool = from_pos[0] == 4 and (
                    slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is on the LEFT, it can be moved up, down or right
            acceptable_left: bool = from_pos[1] == 0 and (
                    slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT
            )
            # if it is on the RIGHT, it can be moved up, down or left
            acceptable_right: bool = from_pos[1] == 4 and (
                    slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT
            )
        # if the piece position is in a corner
        else:
            # if it is in the upper left corner, it can be moved to the right and down
            acceptable_top: bool = from_pos == (0, 0) and (
                    slide == Move.BOTTOM or slide == Move.RIGHT)
            # if it is in the lower left corner, it can be moved to the right and up
            acceptable_left: bool = from_pos == (4, 0) and (
                    slide == Move.TOP or slide == Move.RIGHT)
            # if it is in the upper right corner, it can be moved to the left and down
            acceptable_right: bool = from_pos == (0, 4) and (
                    slide == Move.BOTTOM or slide == Move.LEFT)
            # if it is in the lower right corner, it can be moved to the left and up
            acceptable_bottom: bool = from_pos == (4, 4) and (
                    slide == Move.TOP or slide == Move.LEFT)
        # check if the move is acceptable
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        # if it is
        if acceptable:
            # take the piece
            piece = self._board[from_pos]
            # if the player wants to slide it to the left
            if slide == Move.LEFT:
                # for each column starting from the column of the piece and moving to the left
                for i in range(from_pos[1], 0, -1):
                    # copy the value contained in the same row and the previous column
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], i - 1)]
                # move the piece to the left
                self._board[(from_pos[0], 0)] = piece
            # if the player wants to slide it to the right
            elif slide == Move.RIGHT:
                # for each column starting from the column of the piece and moving to the right
                for i in range(from_pos[1], self._board.shape[1] - 1, 1):
                    # copy the value contained in the same row and the following column
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], i + 1)]
                # move the piece to the right
                self._board[(from_pos[0], self._board.shape[1] - 1)] = piece
            # if the player wants to slide it upward
            elif slide == Move.TOP:
                # for each row starting from the row of the piece and going upward
                for i in range(from_pos[0], 0, -1):
                    # copy the value contained in the same column and the previous row
                    self._board[(i, from_pos[1])] = self._board[(
                        i - 1, from_pos[1])]
                # move the piece up
                self._board[(0, from_pos[1])] = piece
            # if the player wants to slide it downward
            elif slide == Move.BOTTOM:
                # for each row starting from the row of the piece and going downward
                for i in range(from_pos[0], self._board.shape[0] - 1, 1):
                    # copy the value contained in the same column and the following row
                    self._board[(i, from_pos[1])] = self._board[(
                        i + 1, from_pos[1])]
                # move the piece down
                self._board[(self._board.shape[0] - 1, from_pos[1])] = piece
        return acceptable


class MonteCarloPlayer(Player):
    def __init__(self, player_id: int, mcts_steps: int) -> None:
        super().__init__()
        self.player_id = player_id
        self.cache: dict[tuple[tuple[int], int], 'Node'] = dict()
        self.mcts_steps = mcts_steps

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        games = 70  # 70
        # Montecarlo whole process
        for _ in range(self.mcts_steps):
            history = self.selection(game)
            selected_node = history[-1]  # history.pop()
            expanded = self.expansion(selected_node)
            wins, draws = self.simulation(expanded, games)
            # adjust backprop for opponent nodes
            self.backpropagation(wins, draws, games, expanded)
        best_child = max(
            self.cache[(tuple(game.get_board().ravel()), (game.current_player_idx + 1) % 2)].childs.items(),
            key=lambda x: x[0].value())
        # game.print()
        return best_child[1]

    def selection(self, game: 'Game'):
        if (tuple(game.get_board().ravel()), (game.current_player_idx + 1) % 2) in self.cache:
            root = self.cache[(tuple(game.get_board().ravel()), (game.current_player_idx + 1) % 2)]
        else:
            # the player that generated the board is the previous one
            root = Node(game.get_board(), (game.current_player_idx + 1) % 2)
            self.cache[(tuple(game.get_board().ravel()), (game.current_player_idx + 1) % 2)] = root
            root.generate_childs()
            # avoiding redundancy
            for nd, mv in root.childs.copy().items():
                if (tuple(nd.state.ravel()), nd.player) in self.cache:
                    root.childs[self.cache[
                        (tuple(nd.state.ravel()), nd.player)]] = mv
                    root.childs.pop(nd)
                else:
                    self.cache[(tuple(nd.state.ravel()), nd.player)] = nd
        # traverse the tree to get max ucb leaf node
        visited = set()
        history = [root]
        visited.add(root)
        while root.childs:
            next_child = root.get_max_ucb_child()[0]
            if tuple(next_child.state.ravel()) in visited:
                break
            else:
                visited.add(tuple(next_child.state.ravel()))
            history.append(next_child)
            if next_child.visits == 0:
                break
            root = next_child
        return history

    @staticmethod
    def get_random_move(state: np.ndarray, player_id: int):
        game_tmp = Game()
        game_tmp._board = state.copy()
        game_tmp.current_player_idx = player_id
        possible_moves = next_accetptable_moves(game_tmp, player_id)
        return possible_moves[random.randint(0, len(possible_moves) - 1)]

    def expansion(self, node: 'Node') -> 'Node':
        if node.visits == 0:
            return node
        node.generate_childs()
        for nd, mv in node.childs.copy().items():
            if (tuple(nd.state.ravel()), nd.player) in self.cache:
                if (not self.cache[(tuple(nd.state.ravel()), nd.player)].parent
                        or self.cache[(tuple(nd.state.ravel()), nd.player)].parent.visits == 0
                ):
                    self.cache[(tuple(nd.state.ravel()), nd.player)].parent = node
                node.childs[self.cache[
                    (tuple(nd.state.ravel()), nd.player)]] = mv
                node.childs.pop(nd)
            else:
                self.cache[(tuple(nd.state.ravel()), nd.player)] = nd
        if len(node.childs.items()) == 0:
            return node
        else:
            return node.get_max_ucb_child()[0]

    def simulation(self, node: 'Node', n_games: int) -> tuple[int, int]:  # winning, drawing
        return node.simulate_games(n_games)

    def backpropagation(self, wins: int, draws: int, n_games: int, simulated_node: 'Node'):
        visited = set()
        tmp: 'Node' = simulated_node
        while tmp.parent:
            tmp = tmp.parent
            wins = n_games - wins - draws
            if tuple(tmp.state.ravel()) in visited:
                break
            else:
                visited.add(tuple(tmp.state.ravel()))
            tmp.update_params(wins, draws, n_games)


class Node:
    def __init__(self, board: np.ndarray, player: int, move: tuple[tuple[int, int], Move] = None, parent=None):
        self.state = board.copy()
        self.player = player  # the player that generated the current board
        self.wins = 0
        self.draws = 0
        self.visits = 0
        self.move_used = move
        self.parent = parent
        tmp_game = Game()
        tmp_game._board = board.copy()
        tmp_game.current_player_idx = player
        self.over = tmp_game.check_winner()
        tmp_game.current_player_idx = (player + 1) % 2
        self.next_moves = next_accetptable_moves(tmp_game, (player + 1) % 2)
        self.childs: dict[Node, Move] = dict()

    def move(self) -> tuple[tuple[int, int], 'Move']:
        return self.move_used

    def generate_childs(self):
        self.childs = {self.expand_child(mv): mv for mv in self.next_moves} if self.over == -1 else {}

    def calculate_ucb(self, parent_visits) -> float:
        if self.visits == 0:
            return math.inf
        parent_node_visits = self.parent.visits
        exploration_term = (math.sqrt(2.0)
                            * math.sqrt(math.log(parent_node_visits) / self.visits))
        value = self.value() + exploration_term
        return value

    def value(self) -> float:
        if self.visits == 0:
            return 0
        success_percentage = (self.wins + self.draws) / self.visits
        return success_percentage

    def expand_child(self, move: tuple[tuple[int, int], Move]):
        if self.over != -1:
            return None
        monte_game = MonetCarloGame()
        next_state = monte_game.simulate_move(self.state, move, (self.player + 1) % 2)
        new_child = Node(next_state, (self.player + 1) % 2, move, parent=self)
        return new_child

    def get_max_ucb_child(self):
        return max(self.childs.items(), key=lambda x: x[0].calculate_ucb(self.visits))

    def simulate_games(self, steps: int) -> tuple[int, int]:
        if self.over == self.player:
            self.update_params(steps, 0, steps)
            return steps, 0
        elif self.over == (self.player + 1) % 2:
            self.update_params(0, 0, steps)
            return 0, 0  # other player has won
        winning = 0
        drawing = 0
        for _ in range(steps):
            game_env = MonetCarloGame()
            game_env._board = self.state.copy()
            game_env.current_player_idx = self.player
            over = game_env.play(MyRandomPlayer(), MyRandomPlayer())
            if over == self.player:
                winning += 1
            elif over == -1:
                drawing += 1
        self.update_params(winning, drawing, steps)
        return winning, drawing

    def update_params(self, new_wins: int, new_draws: int, total: int):
        self.wins += new_wins
        self.draws += new_draws
        self.visits += total

    def __str__(self):
        return str(self.state) + "--p: " + str(self.player) + " --wins" + str(self.wins) + " --draws" + str(self.draws)

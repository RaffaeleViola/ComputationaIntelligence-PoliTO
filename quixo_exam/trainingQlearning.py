from game import Move, Game, Player
import random
from tqdm import tqdm
import numpy as np
from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from quixo_exam.qtable import Qtable
from quixo_exam.main import RandomPlayer
from quixo_exam.training import next_acts, is_accetptable


class QPlayer(Player):
    def __init__(self, qtab: Qtable, player) -> None:
        super().__init__()
        self.qtable = qtab
        self.epsilon = None
        self.player = player

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        mv = epsilon_greedy_policy(self.qtable, game, self.epsilon, self.player)
        return mv


class MyGame(Game):
    def __init__(self):
        super().__init__()

    def play(self, player1: Player, player2: Player):
        state_history = [tuple(self.get_board().ravel())]
        actions_history = []
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
                ok = self.__move(from_pos, slide, self.current_player_idx)
                if ok:
                    if self.current_player_idx == 0:
                        actions_history.append((from_pos, slide))
                    else:
                        state_history.append(tuple(self.get_board().ravel()))
            # self.print()
            steps += 1
            if steps == 100:
                return -1, state_history, actions_history
            winner = self.check_winner()
        return winner, state_history, actions_history

    def __move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
        '''Perform a move'''
        if player_id > 2:
            return False
        # Oh God, Numpy arrays
        prev_value = deepcopy(self._board[(from_pos[1], from_pos[0])])
        acceptable = self.__take((from_pos[1], from_pos[0]), player_id)
        if acceptable:
            acceptable = self.__slide((from_pos[1], from_pos[0]), slide)
            if not acceptable:
                self._board[(from_pos[1], from_pos[0])] = deepcopy(prev_value)
        return acceptable

    def __take(self, from_pos: tuple[int, int], player_id: int) -> bool:
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

    def __slide(self, from_pos: tuple[int, int], slide: Move) -> bool:
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
        # print(slide, end=" ")
        # print(Move.RIGHT, end=" ")
        # print(slide == Move.RIGHT)
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


def backpropagation(qtable: Qtable, states: list, actions: list, reward, learning_rate, gamma):
    default = 0.0
    next_state = None
    for act, state in zip(reversed(actions), reversed(states)):
        fut_max = max(qtable.table[next_state].values()) if next_state else default
        qtable.table[state][act] = qtable.table[state][act] + learning_rate * (
                reward + gamma * fut_max - qtable.table[state][act])
        next_state = state
    return qtable


def next_accetptable_moves(state: Game, player: int):
    actions = next_acts(state, player)
    return [(act, direct) for act in actions for direct in [Move.TOP, Move.LEFT, Move.RIGHT, Move.BOTTOM]
            if is_accetptable(act, direct, state)]


def epsilon_greedy_policy(qtable: Qtable, state: Game, epsilon: float, player: int):
    random_int = random.uniform(0, 1)
    actions = next_accetptable_moves(state, player)
    if random_int > epsilon and tuple(state.get_board().ravel()) in qtable.get_table():
        return max(actions, key=lambda act: qtable.get_table()[tuple(state.get_board().ravel())][act])
    else:
        action = actions[random.randint(0, len(actions) - 1)]
        if tuple(state.get_board().ravel()) not in qtable.get_table():
            tmp = {mv: 0.0 for mv in actions}
            qtable.get_table()[tuple(state.get_board().ravel())] = tmp
    return action


def training():
    # Training parameters
    n_training_episodes = 10_000
    learning_rate = 0.7

    # Environment parameters
    gamma = 0.95

    # Exploration parameters
    max_epsilon = 1.0
    min_epsilon = 0.01
    decay_rate = 0.0005
    tab = Qtable()
    player1 = RandomPlayer()
    player0 = QPlayer(tab, 0)
    for episode in tqdm(range(n_training_episodes)):
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        player0.epsilon = epsilon
        for n in [0]:
            # Reset the environment
            env = MyGame()
            # simulating game
            done, state_history, actions_history = env.play(player0, player1)
            # updating states
            reward = -(2*done - 1) if done != -1 else 0.1  # +1 win -1 lose 0.1 draw
            if len(state_history) != len(actions_history):
                # print(state_history)
                # print(actions_history)
                state_history.pop()
            player0.qtable = backpropagation(player0.qtable, state_history, actions_history, reward, learning_rate, gamma)
    print(player0.qtable.get_table())
    return player0.qtable


training()


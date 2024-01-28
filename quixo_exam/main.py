import math
import random
from game import Game, Move, Player
from quixo_exam.monteCarloTreeSearch import MonteCarloPlayer
from minmax import minmax
from tqdm import tqdm


class RandomPlayer(Player):
    
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        # copy the game to avoid modifying it
        tmp_game = Game()
        tmp_game._board = game.get_board()
        tmp_game.current_player_idx = game.current_player_idx
        montecarlo = MonteCarloPlayer(tmp_game.current_player_idx, mcts_steps=100)
        depth = 4
        if (tmp_game.get_board() == -1).sum() < 6:
            return montecarlo.make_move(tmp_game)
        move, val = minmax(tmp_game, (tmp_game.current_player_idx + 1)%2 , depth, -math.inf, math.inf, tmp_game.current_player_idx)
        # check if the move makes the opponent winning
        check_winner_game = Game()
        check_winner_game._board = tmp_game.get_board()
        check_winner_game.current_player_idx = tmp_game.current_player_idx
        check_winner_game._Game__move(move[0], move[1], tmp_game.current_player_idx)
        # if it is use montecarlo tree search
        if check_winner_game.check_winner() not in [-1, check_winner_game.current_player_idx]:
            return montecarlo.make_move(tmp_game)
        return move


class InputPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        game.print()
        match = {"T": Move.TOP, "B": Move.BOTTOM, "L": Move.LEFT, "R": Move.RIGHT}
        ply = input("format <x-y-T/B/L/R>\n")
        words = ply.strip().split("-")
        x, y, m = int(words[0]), int(words[1]), match[words[2]]
        return (x, y), m


if __name__ == '__main__':
    win_rate = 0
    for _ in tqdm(range(200)):
        g = Game()
        g.print()
        player2 = MyPlayer()
        player1 = RandomPlayer()
        winner = g.play(player1, player2)
        if winner == 1:
            win_rate += 1
        print(f"\n{win_rate}/200\n")


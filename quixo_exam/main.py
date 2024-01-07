import math
import random
from game import Game, Move, Player
from quixo_exam.training import minmax
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
        move, _ = minmax(game, 1, 3, -math.inf, math.inf)
        return move


class InputPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        match = {"T": Move.TOP, "B": Move.BOTTOM, "L": Move.LEFT, "R": Move.RIGHT}
        ply = input("format <x-y-T/B/L/R>\n")
        words = ply.strip().split("-")
        x, y, m = int(words[0]), int(words[1]), match[words[2]]
        return (x, y), m


if __name__ == '__main__':
    win_rate = 0
    for _ in tqdm(range(500)):
        g = Game()
        # g.print()
        player1 = MyPlayer()
        player2 = RandomPlayer()
        winner = g.play(player1, player2)
        if winner == 0:
            win_rate += 1
        # g.print()
        # print(f"Winner: Player {winner}")
        print(f"\n{win_rate}/500\n")

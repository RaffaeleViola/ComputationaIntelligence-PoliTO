import math
import random
from game import Game, Move, Player
from quixo_exam.training import minmax, is_accetptable, next_acts
from tqdm import tqdm


def all_acceptable(game: Game):
    next_actions = next_acts(game, 0)
    for move in next_actions:
        for direct in [Move.TOP, Move.LEFT, Move.RIGHT, Move.BOTTOM]:
            if not is_accetptable(move, direct, game):
                continue
            print((move, direct))
    print()

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
        # all_acceptable(game)
        depth = 4
        minus_one_sum = sum([1 for val in list(game.get_board().ravel()) if val == -1])
        # if minus_one_sum <= 7:
        #     depth = 6
        move, val = minmax(game, 1, depth, -math.inf, math.inf)
        # if val == -1:
        #     print("Losing game: ")
        #     print(game.get_board())
        #     print(move)
        # print((move, val))
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
    draw_rate = 0
    for _ in tqdm(range(100)):
        g = Game()
        # g.print()
        player1 = MyPlayer()
        player2 = RandomPlayer()
        winner = g.play(player1, player2)
        if winner == 0:
            win_rate += 1
        elif winner == -1:
            draw_rate += 1
        # g.print()
        # print(f"Winner: Player {winner}")
        print(f"\n{win_rate}/100\n")
    print(f"\ndraw_rate: {draw_rate}/100\n")

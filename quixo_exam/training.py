"""
QTable => {
            state_table_as_tuple: {
                    (x, y, TOP/RIGHT/LEFt/RIGHT): {
                        Qvalue
                    }
                }
            }
"""
import itertools
from game import Game, Move


# check if a move is acceptable (taken from the game code)
def is_acceptable(board: tuple[tuple[int]], from_pos: tuple[int, int], player_id: int) -> bool:
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
                       ) and (board[from_pos[0]][from_pos[1]] < 0 or board[from_pos[0]][from_pos[1]] == player_id)
    return acceptable


def generate_all_possible_states(player: int):
    def is_valid(state) -> bool:
        move_0 = sum(1 for c in state if c == 0)
        move_1 = sum(1 for c in state if c == 1)
        return (move_0 == move_1
                or (move_0 == (move_1 - 1) and player == 0)
                or (move_0 == (move_1 + 1) and player == 1))

    # filter valid states
    disps = [tuple(disp) for disp in list(itertools.product([0, 1, -1], repeat=15)) if is_valid(disp)]
    return disps


def next_acts(game: Game, player: int):
    res = []
    board = game.get_board()
    for i in range(5):
        if board[0, i] == player or board[0, i] == -1:
            res.append((i, 0))
        if board[4, i] == player or board[4, i] == -1:
            res.append((i, 4))
    for i in range(1, 4):
        if board[i, 0] == player or board[i, 0] == -1:
            res.append((0, i))
        if board[i, 4] == player or board[i, 4] == -1:
            res.append((4, i))
    return res


def is_accetptable(from_pos, slide, game: Game):
    # swapping for coordinates compliance
    from_pos = (from_pos[1], from_pos[0])
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
                       ) and (game.get_board()[from_pos] < 0 or game.get_board()[from_pos] == game.current_player_idx)
    if not acceptable:
        return False
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
    return acceptable


max_cache = dict()
min_cache = dict()


def minmax(game: Game, plyr_id, depth, alpha, beta) -> tuple[tuple[tuple[int, int], Move], float]:
    cache = max_cache if plyr_id == 0 else min_cache
    if tuple(game.get_board().ravel()) in cache:
        return cache[tuple(game.get_board().ravel())]
    plyr_id += 1
    plyr_id %= 2
    over = game.check_winner()
    next_actions = next_acts(game, plyr_id)
    if over != -1 or not next_actions or depth == 0:
        res = -(2 * over - 1) if over != -1 else 0
        return None, res  # 1 for 0 player and -1 for 1 player
    new_g = Game()
    new_g._board = game.get_board()
    new_g.current_player_idx = plyr_id
    best_move = None
    for move in next_actions:
        for direct in [Move.TOP, Move.LEFT, Move.RIGHT, Move.BOTTOM]:
            if not is_accetptable(move, direct, new_g):
                continue
            new_g = Game()
            new_g._board = game.get_board()
            new_g.current_player_idx = plyr_id
            new_g._Game__move(move, direct, plyr_id)
            _, score = minmax(new_g, plyr_id, depth - 1, alpha, beta)
            if plyr_id == 0:  # to maximize
                if score > alpha:
                    alpha = score
                    best_move = (move, direct)
                if score >= beta:
                    break
            else:
                if score < beta:  # to_minimize
                    beta = score
                    best_move = (move, direct)
                if alpha >= beta:
                    break
            if best_move is None:
                best_move = (move, direct)
    if best_move:
        cache[tuple(game.get_board().ravel())] = best_move, alpha
    return best_move, alpha

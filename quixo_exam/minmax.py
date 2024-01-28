import math
import numpy as np
from game import Game, Move


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


def is_accetptable(pos, slide, game: Game):  # it takes standard coordinates x,y (row, col)
    # swapping for coordinates compliance
    from_pos = (pos[1], pos[0])
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


def rotate_board(board: np.ndarray):
    # 90 degree
    # it's clockwise
    r270 = np.rot90(board)
    r180 = np.rot90(r270)
    r90 = np.rot90(r180)
    return r90, r180, r270


def transform_move(cache_item: tuple[tuple[tuple[int, int], Move], float], degree: int) -> tuple[
    tuple[tuple[int, int], Move], float]:
    move, scr = cache_item
    pos = move[0]
    mv = move[1]
    # map_move = {Move.TOP: Move.RIGHT, Move.RIGHT: Move.BOTTOM, Move.BOTTOM: Move.LEFT, Move.LEFT: Move.TOP}
    map_move = {Move.TOP: Move.LEFT, Move.RIGHT: Move.TOP, Move.BOTTOM: Move.RIGHT, Move.LEFT: Move.BOTTOM}
    map_y_into_x = {0: 4, 4: 0, 1: 3, 3: 1, 2: 2}
    p270 = map_y_into_x[pos[1]], pos[0]
    p180 = map_y_into_x[p270[1]], p270[0]
    p90 = map_y_into_x[p180[1]], p180[0]
    if degree == 90:
        return (p90, map_move[mv]), scr
    elif degree == 180:
        return (p180, map_move[map_move[mv]]), scr
    else:
        return (p270, map_move[map_move[map_move[mv]]]), scr


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


def minmax(game: Game, plyr_id, depth, alpha, beta, plyr_to_maximize: int) -> tuple[tuple[tuple[int, int], Move], float]:
    plyr_id += 1
    plyr_id %= 2
    cache = max_cache if plyr_id == plyr_to_maximize else min_cache
    # checking board and rotations in cache
    b90, b180, b270 = rotate_board(game.get_board())
    if (tuple(game.get_board().ravel()), depth) in cache:
        return cache[tuple(game.get_board().ravel()), depth]
    if (tuple(b90.ravel()), depth) in cache:
        return transform_move(cache[tuple(b90.ravel()), depth], 90)
    if (tuple(b180.ravel()), depth) in cache:
        return transform_move(cache[tuple(b180.ravel()), depth], 180)
    if (tuple(b270.ravel()), depth) in cache:
        return transform_move(cache[tuple(b270.ravel()), depth], 270)
    over = game.check_winner()
    next_actions = next_acts(game, plyr_id)
    if over != -1 or not next_actions or depth == 0:
        prev_plr = plyr_id + 1
        prev_plr %= 2
        res = scoring_fun(game, prev_plr, plyr_to_maximize)
        return None, res
    new_g = Game()
    new_g._board = game.get_board()
    new_g.current_player_idx = plyr_id
    best_move = None
    curr_alpha = alpha
    curr_beta = beta
    to_stop = False
    for move in next_actions:
        for direct in [Move.TOP, Move.LEFT, Move.RIGHT, Move.BOTTOM]:
            if not is_accetptable(move, direct, new_g):
                continue
            new_g = Game()
            new_g._board = game.get_board()
            new_g.current_player_idx = plyr_id
            new_g._Game__move(move, direct, plyr_id)
            _, score = minmax(new_g, plyr_id, depth - 1, curr_alpha, curr_beta, plyr_to_maximize)
            if plyr_id == plyr_to_maximize:  # to maximize
                if score > curr_alpha:
                    curr_alpha = score
                    best_move = (move, direct)
                if curr_alpha >= curr_beta:
                    to_stop = True
                    break
            else:
                if score < curr_beta:  # to_minimize
                    curr_beta = score
                    best_move = (move, direct)
                if curr_alpha >= curr_beta:
                    to_stop = True
                    break
            if best_move is None:
                best_move = (move, direct)
        if to_stop:
            break
    score_val = curr_alpha if plyr_id == plyr_to_maximize else curr_beta
    if best_move:
        cache[tuple(game.get_board().ravel()), depth] = best_move, score_val
    return best_move, score_val
